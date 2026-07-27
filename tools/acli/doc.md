# Atlassian CLI (`acli`)

Official command-line client for Jira, Confluence, and Bitbucket. Needed for any read/write Jira operation an agent runs against a real project (ticket search, transitions, reports).

- **Install docs:** https://developer.atlassian.com/cloud/acli/guides/install-acli/
- **Command reference:** https://developer.atlassian.com/cloud/acli/reference/commands/

## Verify

```bash
acli --version
```

## Authenticate

```bash
acli jira auth login --web                                                  # browser OAuth flow
acli jira auth login --site "yoursite.atlassian.net" --email "you@co.com" --token   # API token via stdin
acli jira auth status                                                        # check current auth
```

## Common commands

```bash
acli jira workitem search --fields status,assignee,issuetype,summary,key -q "<JQL>"
acli jira workitem view <KEY> --fields '...' --json     # per-issue fetch (allows customfields + dates; search does not)
```

**Gotcha:** `workitem search --fields` rejects `resolutiondate`, `created`, `updated`, and any `customfield_*` ("field not allowed") — it only allows `assignee,status,issuetype,summary,key`. To get points/dates, filter by them in JQL and fetch per-issue with `workitem view --json`, which does allow customfields and dates.

Each CLI version is supported for 6 months after release — keep it current.
