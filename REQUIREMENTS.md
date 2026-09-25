# Functional Requirements & User Stories

**System:** NL-to-Dashboard Agent  
**Version:** 0.1

## Actors

| Actor | Description |
|---|---|
| Analyst | Query permitted tables, pin and share widgets |
| Viewer | Authenticated, no table access for a dataset |
| Shared recipient | Granted access to a pinned widget |
| Agent | Parse NL, call MCP, emit chart specs |
| MCP server | ACL, cache, artifact store |
| Front-end | Render specs; pin / share UI |

## Functional requirements

- **FR-1** Accept free-text questions from an authenticated user.
- **FR-2** Split one question into intents (point, trend, aggregate).
- **FR-3** Resolve each intent via MCP schema metadata; do not invent columns.
- **FR-4** All warehouse access goes through MCP.
- **FR-5** Reject if the caller role cannot read referenced tables.
- **FR-6** Apply warehouse RLS on every query and cache hit.
- **FR-7** Cache key = fingerprint(normalized SQL) + role.
- **FR-8** Cache hits still pass table ACL and RLS.
- **FR-9** Chart map: metric → KPI; time series → line/area; period total → bar.
- **FR-10** Agent returns JSON spec only (no HTML/React).
- **FR-11** Multi-intent questions render as one board.
- **FR-12** Widget shows fresh vs cached.
- **FR-13** Pin stores widget_id, chart_type, sql, spec, owner, shared_with, created_at.
- **FR-14** Owner can reload pinned widgets onto their dashboard.
- **FR-15** Owner can share a widget with named users.
- **FR-16** Load requires owner or shared_with AND table/RLS permission.
- **FR-17** Same fingerprint + authorized role reuses cache (query runs once).
- **FR-18** Read-only tools only.
- **FR-19** Log ask, execute, cache hit, pin, share, load, deny.
- **FR-20** Denials appear as error widgets, not empty boards.

Out of scope v0.1: agent SQL without schema tool, cross-warehouse joins, writes, semantic question matching, TTL/refresh policy.

## User stories

### US-01 Ask a multi-part question
As an analyst I want one question to cover yesterday, trend, and MTD so I do not write SQL.

Given Alice can read meetings, when she asks the three-part meetings question, then three intents run, and the board shows KPI + line + MTD widget, each with a declarative spec.

### US-02 Right chart type
As an analyst I want chart type chosen from data shape.

Point → KPI; 30-day series → line/area; MTD → bar or large number. Spec is JSON.

### US-03 Repeat uses cache
As an analyst I want the second equivalent question to skip the warehouse.

Given the 30-day trend already ran, when Alice or Bob (same role) asks it again, then source is cache and warehouse is not called.

### US-04 Pin to my dashboard
As an analyst I want to pin a widget so I can reopen it without re-asking.

Pin persists artifact fields; load re-renders the spec; permissions are re-checked.

### US-05 Share with a colleague
As an analyst I want to share a pinned widget with Bob so he reuses the query and cache.

Bob can load after share. Carol, not shared and without table access, cannot.

### US-06 Deny without table access
As a viewer I want a clear denial instead of leaked or empty data.

Carol asking meetings yesterday gets permission denied, no rows, no cache write for her role.

### US-07 Share does not bypass ACL
As a security owner I want sharing to grant artifact visibility only.

shared_with plus failed table/RLS still denies. Cache never serves a privileged result to a weaker role.

### US-08 Review as different users
As a reviewer I want to switch Alice / Bob / Carol to verify allow, cache, deny.

### US-09 Freshness visible
As an analyst I want fresh vs cached on each widget.

### US-10 Front-end owns rendering
As a front-end engineer I want only a spec so we keep Vega-Lite or ECharts and can swap later.

## Traceability

| Story | Requirements |
|---|---|
| US-01 | FR-1 FR-2 FR-3 FR-4 FR-11 |
| US-02 | FR-9 FR-10 |
| US-03 | FR-7 FR-8 FR-12 |
| US-04 | FR-13 FR-14 |
| US-05 | FR-15 FR-17 |
| US-06 | FR-5 FR-20 |
| US-07 | FR-5 FR-6 FR-8 FR-16 |
| US-08 | FR-5 FR-16 |
| US-09 | FR-12 FR-19 |
| US-10 | FR-10 FR-13 |
