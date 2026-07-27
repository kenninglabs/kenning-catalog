# Service Communication Map — Generic Template

**Triggers:** documenting how services in a project talk to each other (REST/Kafka/RPC/shared DBs) for the first time, or keeping an existing map current after a cross-service change.

> **Project-independent.** Standard structure for documenting how services in a project talk to each other. Distilled from working maps for multi-service architectures.

## Why this exists

Distributed systems have many ways services interact: REST/Feign, Kafka, RPC, shared DBs, file drops. A service-communication map is the single artifact someone reads to understand "who calls whom, with what protocol, carrying what data" — without having to grep four codebases.

It's the **architecture diagram + protocol matrix in one document**.

## Mandatory sections

A complete map has 5 sections in this order:

### 1. Service Overview (ASCII diagram)

A box-and-arrow diagram showing the major service tiers and their dependencies. ASCII because it renders in any tool (terminal, GitHub, docs site, IDE, AI tool).

```
┌─────────────────────────────────────────┐
│ FRONTEND                                 │
│   <frontend-1>, <frontend-2>             │
└─────────────────┬────────────────────────┘
                  │ <protocol>
                  ▼
┌─────────────────────────────────────────┐
│ API GATEWAY LAYER                        │
│   <gateway-service>                      │
└──────┬──────────────────────┬───────────┘
       │                      │
       ▼                      ▼
┌──────────────┐     ┌──────────────────┐
│ <core-svc-1> │────▶│ <core-svc-2>     │
│              │Feign│                  │
└──────────────┘     └──────────────────┘
```

Tier organization (top-to-bottom):
1. **Frontend** — UIs, mobile apps, partner-facing portals
2. **API Gateway / Auth** — Kong, Nginx, custom gateway, SSO
3. **Core services** — business logic, the things the gateway routes to
4. **External proxies** — services that wrap third-party APIs (banking, payment processors)
5. **Async layer** — Kafka producers/consumers, schedulers, queue workers
6. **Data tier** — databases, caches (often shown as a sidebar rather than a tier)

### 2. Communication Protocols

Sub-sections per protocol. Each sub-section is a table with consistent columns.

**REST / Feign / RPC (Synchronous)** — table format:

```markdown
| From | To | Via | Headers | Purpose |
|------|----|-----|---------|---------|
| <service-A> | <service-B> | Feign / REST / gRPC | `X-TENANT-ID`, `Authorization` | <what this call does> |
```

Required columns: From, To, Via (protocol/library), Headers (anything special), Purpose. Optional: timeout, retry policy, circuit-breaker config.

**Kafka / Async** — table format:

```markdown
| Topic | Producer | Consumer(s) | Payload | Notes |
|-------|----------|-------------|---------|-------|
| <topic-name> | <producer-service> | <consumer-service-1>, <consumer-2> | <payload type> | partitions, ordering guarantees, retry policy |
```

Required columns: Topic, Producer, Consumer, Payload. Optional: partition count, retention, error handling.

**Other async/batch** (file drops, scheduled jobs, webhooks) — table format depends on shape, but always include: source, destination, trigger condition.

### 3. Internal Service URLs (k8s / service mesh)

Single table with cluster-internal addresses for direct service-to-service calls (not through the gateway):

```markdown
| Service | Internal URL |
|---------|-------------|
| <service-A> | `<service-A>.<namespace>.svc.cluster.local:8080` |
```

This is the source of truth for "what does service A use as its `feign.client.url` for service B." Frontend → gateway → service flows go through public URLs; service → service flows go through these.

### 4. Databases

Single table mapping each service to its persistent stores:

```markdown
| Service | Database | Type | Tenancy |
|---------|----------|------|---------|
| <service> | MongoDB / PostgreSQL / Redis | Per-tenant / Shared / Per-environment | Multi-tenant via header? Single-tenant? |
```

Include: type (Mongo, Postgres, Redis, Elasticsearch, etc.), tenancy model (per-tenant DB? shared DB with tenant_id column? per-env?), and whether reads/writes go through a service or are direct.

### 5. Open Questions / Gaps (optional)

If the map is incomplete or there's a known cross-cutting concern not yet documented, list it explicitly:

```markdown
## Known Gaps

- [ ] <protocol-X> between <service-A> and <service-B> — payload schema not yet documented
- [ ] Retry policy for <topic-Y> — values vary across env, need consolidation
```

This is honest about what the map doesn't cover yet.

## Rules

### 1. The diagram is the entry point

A reader who's never seen the system should be able to look at the diagram and answer "what are the major services, and who depends on whom?" in 30 seconds.

If the diagram has more than ~12 boxes, split into per-domain sub-diagrams instead of a single mega-diagram.

### 2. Every arrow in the diagram has a row in §2

If you draw an arrow from A to B in the diagram, there's a row in the REST or Kafka table that says what's on that arrow. No silent arrows.

### 3. Update on every cross-service change

A change is "cross-service" if it touches a Feign client, a Kafka producer/consumer, or a service URL. PRs that include those should also update this file.

A stale communication map is worse than no map — it actively misleads.

### 4. Names match deployment artifacts

Use the same service name as appears in argocd / k8s / docker-compose. Don't invent abstract names ("auth-layer") that don't exist as a real deployment unit.

### 5. Keep it under one screen per protocol section

If the REST table has 30 rows, you've got too many cross-service calls or the map is too coarse. Either split into multiple maps (per domain) or consolidate calls into a smaller number of higher-level rows.

## Project-specific maps

Specific service names, real Feign clients, real Kafka topics for your project belong in your own project's docs, not here. This file is the template; your project-specific equivalent has the actual diagram + tables filled in for your services.
