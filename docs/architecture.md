# Architecture: NL-to-Dashboard Agent (OpenCode harness)

## Overview

Conversational analytics path: natural language in, chart widgets out.

```
warehouse -> MCP (ACL + cache + artifacts) -> chart spec -> front-end renderer -> pin/share
```

The agent never touches the warehouse directly. Every query, cache hit, and permission check flows through the MCP server, so access control lives in one place.

## Architecture diagram

```
+---------------------------+     +---------------------------+
|  Browser dashboard        |     |  OpenCode TUI             |
|  (shadcn dashboard-01     |     |  (developers)             |
|   shell, widgets)         |     |                           |
+-------------+-------------+     +-------------+-------------+
              |                                 |
              +----------------+----------------+
                               |
                               v
+-------------------------------------------------------------+
|  AGENT LAYER — OpenCode harness                             |
|  - model-agnostic loop (Claude, GPT, others via LiteLLM)    |
|  - MCP client built in                                       |
|  - AGENTS.md for project instructions                        |
|  - orchestrates: intent parsing, chart selection, spec emit  |
+-----------------------------+-------------------------------+
                              |
                              | MCP protocol (tools + resources)
                              v
+-------------------------------------------------------------+
|  MCP SERVER — enforcement point                              |
|  - warehouse connection                                       |
|  - table-level + row-level permissions (RLS)                 |
|  - cache keyed on sql fingerprint + role                     |
|  - artifact store (pinned + shared widgets)                  |
+-----------------------------+-------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|  DATA LAYER — warehouse                                      |
+-------------------------------------------------------------+
```

## Layer responsibilities

### User layer

- Browser dashboard: shadcn/ui dashboard-01 shell (inset sidebar, header, stat cards, chart panel). Renders agent-emitted JSON specs via Vega-Lite or ECharts.
- OpenCode TUI: developer-facing harness for building and debugging the agent.

### Agent layer (OpenCode)

- Runs the tool-calling loop against the MCP server.
- Splits a user request into intents (e.g., yesterday count, 30-day trend, month-to-date).
- Selects chart type per data shape.
- Emits a declarative JSON spec — never rendered pixels.

### Data and artifact layer (MCP server)

- Single enforcement point for table ACL and row-level security.
- Cache key: `fingerprint(sql) + role` — not user name alone. Two users asking the same thing can see different rows.
- Re-checks permissions on every cache hit and every artifact load.
- Stores pinned widgets: chart type, widget ID, SQL, spec.

### Data layer

- The warehouse. No direct access from the agent.

## Why OpenCode

- MIT license, model-agnostic (75+ providers), strong MCP support.
- No sandbox/filesystem machinery needed — this agent is a tool-calling loop, not a coding agent.
- Alternatives considered: smolagents (most minimal, code-as-action), OpenAI Agents SDK (fastest to ship, provider-agnostic), Pi (best cost-per-task via context discipline).

## Design rules

1. Chart component emits a spec, not pixels.
2. Cache key is `fingerprint(sql) + role`.
3. MCP re-checks table ACL on cache hits and artifact loads.
4. Artifact visibility is owner or `shared_with`, plus table ACL.
5. Agent never bypasses MCP — no direct warehouse credentials.

## Open questions

- Cache TTL for time-sensitive queries (yesterday's count goes stale fast).
- Refresh-on-view vs scheduled refresh for pinned widgets.
- Intent matching: exact fingerprint vs semantic similarity for shared widgets.
