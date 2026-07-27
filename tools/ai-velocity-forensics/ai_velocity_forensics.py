#!/usr/bin/env python3
"""
AI-usage velocity forensics for a git repo.

Infers whether commits were likely AI-assisted by analysing implementation
*efficiency* signals: inter-commit cadence, net-LOC-per-active-hour bursts,
single-commit size vs prior gap, commit-message style, and hard Copilot trailers.

Forensic premise (and its limits):
  - Commit timing/velocity is CIRCUMSTANTIAL. High kept-LOC in a short window can
    mean AI, but also generated boilerplate, copy-paste, or scaffolding.
  - The only HARD evidence of AI is explicit Copilot/AI trailers & messages.
  - We separate "logic" LOC from generated/boilerplate (xml/json/properties/lock/
    build/dto/mapper) and from test files so velocity reflects real authoring.

Usage: ai_velocity_forensics.py <repo_path> <since=YYYY-MM-DD> [label] [base_branch]
       base_branch defaults to "main" -- pass "master" (or your default branch) if that's
       what this repo uses; it's the branch every other branch's lifespan is measured against.
"""
import subprocess, sys, re, json
from collections import defaultdict

REPO = sys.argv[1]
SINCE = sys.argv[2]
LABEL = sys.argv[3] if len(sys.argv) > 3 else REPO.split("/")[-1]
BASE_BRANCH = sys.argv[4] if len(sys.argv) > 4 else "main"

def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True).stdout

# ---- thresholds ----
BURST_GAP_MIN = 45          # commits <45 min after the author's previous commit = same session
BIG_LOGIC = 250             # net logic LOC in one commit
FAST_BIG = 30               # ...landed <30 min after prior commit by same author => velocity flag
HIGH_LPH = 400              # sustained kept-logic LOC/hour across a session => velocity flag

GEN_PAT = re.compile(r'(\.xml|\.json|\.properties|\.ya?ml|\.lock|\.gradle|\.md|/dto/|dto\.java$|mapper|/generated/|changelog|liquibase|package-lock|\.sql)', re.I)
TEST_PAT = re.compile(r'(test/|tests/|/test|Test\.java$|Tests\.java$|spec\.|\.spec)', re.I)

def classify(path):
    if TEST_PAT.search(path): return "test"
    if GEN_PAT.search(path):  return "gen"
    return "logic"

# ---- pull commits: dedup across all branches ----
raw = git("log","--all","--no-merges",f"--since={SINCE}",
          "--pretty=format:@@@|%H|%an|%at|%s","--numstat")
commits = {}   # hash -> dict
cur = None
for line in raw.splitlines():
    if line.startswith("@@@|"):
        _,h,an,at,subj = line.split("|",4)
        an = an.strip()
        cur = {"h":h,"an":an,"at":int(at),"subj":subj,
               "logic_add":0,"logic_del":0,"gen_add":0,"gen_del":0,
               "test_add":0,"test_del":0,"files":0}
        commits[h]=cur
    elif cur is not None and line.strip():
        parts=line.split("\t")
        if len(parts)==3:
            a,d,path=parts
            a=int(a) if a.isdigit() else 0
            d=int(d) if d.isdigit() else 0
            k=classify(path)
            cur[f"{k}_add"]+=a; cur[f"{k}_del"]+=d; cur["files"]+=1

cl=list(commits.values())
cl.sort(key=lambda c:c["at"])

# ---- copilot / AI hard-signal commits (message text) ----
ai_msg = git("log","--all","--no-merges",f"--since={SINCE}","--format=%an|%s")
ai_hits=defaultdict(int)
for ln in ai_msg.splitlines():
    if "|" not in ln: continue
    an,subj=ln.split("|",1)
    an=an.strip()
    if re.search(r'copilot|chatgpt|claude|cursor|generated with|aider|\bgpt\b',subj,re.I):
        ai_hits[an]+=1
# autofix trailers
trl = git("log","--all","--no-merges",f"--since={SINCE}",
          "--format=%an|%(trailers:key=Co-authored-by,valueonly)")
autofix=defaultdict(int)
for ln in trl.splitlines():
    if "copilot" in ln.lower():
        an=ln.split("|",1)[0].strip()
        autofix[an]+=1

# ---- per-author velocity ----
by_auth=defaultdict(list)
for c in cl: by_auth[c["an"]].append(c)

print(f"\n{'='*78}\n  {LABEL}  —  AI-velocity forensics  (since {SINCE})\n{'='*78}")
print(f"Unique non-merge commits analysed: {len(cl)}")

flags_global=[]
rows=[]
for an,cs in by_auth.items():
    cs.sort(key=lambda c:c["at"])
    logic=sum(c["logic_add"] for c in cs)
    gen=sum(c["gen_add"] for c in cs)
    test=sum(c["test_add"] for c in cs)
    span_days=(cs[-1]["at"]-cs[0]["at"])/86400 if len(cs)>1 else 0
    active_days=len({c["at"]//86400 for c in cs})
    # message style: avg subject length, % terse (<25 chars)
    avglen=sum(len(c["subj"]) for c in cs)/len(cs)
    terse=sum(1 for c in cs if len(c["subj"])<25)/len(cs)
    # velocity flags: big logic commit shortly after prior same-author commit
    vflags=[]
    sessions=[]  # (start,end,logic_loc)
    sess_start=cs[0]["at"]; sess_loc=cs[0]["logic_add"]; prev=cs[0]["at"]
    for i,c in enumerate(cs):
        gap=(c["at"]-cs[i-1]["at"])/60 if i>0 else None
        if gap is not None and gap<=BURST_GAP_MIN:
            sess_loc+=c["logic_add"]
        else:
            if i>0: sessions.append((sess_start,prev,sess_loc))
            sess_start=c["at"]; sess_loc=c["logic_add"]
        prev=c["at"]
        if gap is not None and c["logic_add"]>=BIG_LOGIC and gap<=FAST_BIG:
            vflags.append((c["h"][:9],c["logic_add"],round(gap),c["subj"][:48]))
    sessions.append((sess_start,prev,sess_loc))
    # peak sustained logic LOC/hr over a multi-commit session
    peak_lph=0; peak_sess=None
    for s,e,loc in sessions:
        dur_h=(e-s)/3600
        if dur_h>=0.25 and loc>=BIG_LOGIC:
            lph=loc/dur_h
            if lph>peak_lph: peak_lph=lph; peak_sess=(loc,round(dur_h,2))
    rows.append({"an":an,"commits":len(cs),"logic":logic,"gen":gen,"test":test,
                 "active_days":active_days,"span":round(span_days,1),
                 "avglen":round(avglen),"terse":round(terse*100),
                 "peak_lph":round(peak_lph),"peak_sess":peak_sess,
                 "vflags":vflags,
                 "copilot_msg":ai_hits.get(an,0),"autofix":autofix.get(an,0)})

rows.sort(key=lambda r:-r["logic"])
print(f"\n{'AUTHOR':<22}{'cmt':>4}{'logicLOC':>9}{'genLOC':>7}{'testLOC':>8}{'actDay':>7}{'msgLen':>7}{'terse%':>7}{'peakLPH':>8}{'CoPilot':>8}")
print("-"*95)
for r in rows:
    cop=f"{r['copilot_msg']}m/{r['autofix']}a"
    print(f"{r['an']:<22}{r['commits']:>4}{r['logic']:>9}{r['gen']:>7}{r['test']:>8}{r['active_days']:>7}{r['avglen']:>7}{r['terse']:>6}%{r['peak_lph']:>8}{cop:>8}")

print(f"\n--- VELOCITY FLAGS (big logic commit <{FAST_BIG}min after prior same-author commit) ---")
any_flag=False
for r in rows:
    for h,loc,gap,subj in r["vflags"]:
        any_flag=True
        print(f"  {r['an']:<20} {h} +{loc} logic LOC, {gap}min gap :: {subj}")
if not any_flag: print("  (none — no anomalous fast-large logic bursts)")

print(f"\n--- PEAK SUSTAINED SESSIONS (logic LOC/hr over a >=15min multi-commit session) ---")
for r in rows:
    if r["peak_sess"]:
        loc,dur=r["peak_sess"]
        print(f"  {r['an']:<20} {r['peak_lph']:>5} LOC/hr  ({loc} logic LOC over {dur}h)")

# ---- branch lifespan/efficiency ----
print(f"\n--- BRANCH LIFESPAN & EFFICIENCY (unique vs {BASE_BRANCH}, since {SINCE}) ---")
branches=git("branch","-r").splitlines()
brows=[]
for b in branches:
    b=b.strip()
    if "HEAD" in b or b.endswith(f"/{BASE_BRANCH}"): continue
    log=git("log","--no-merges",f"--since={SINCE}","--pretty=format:%at|%an",f"{BASE_BRANCH}..{b}")
    ls=[x for x in log.splitlines() if "|" in x]
    if not ls: continue
    ats=sorted(int(x.split("|")[0]) for x in ls)
    owner=ls[-1].split("|",1)[1].strip()
    dur_d=(ats[-1]-ats[0])/86400
    ns=git("log","--no-merges",f"--since={SINCE}","--pretty=tformat:","--numstat",f"{BASE_BRANCH}..{b}")
    add=sum(int(x.split('\t')[0]) for x in ns.splitlines() if x.split('\t')[0].isdigit())
    brows.append((len(ls),round(dur_d,1),add,owner,b.replace("origin/","")))
brows.sort(key=lambda x:-x[2])
print(f"{'cmt':>4}{'days':>6}{'LOC+':>8}  {'owner':<20} branch")
for cmt,dur,add,owner,b in brows[:30]:
    print(f"{cmt:>4}{dur:>6}{add:>8}  {owner[:18]:<20} {b[:55]}")
