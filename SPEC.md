# NL-to-Dashboard Agent — Architecture Spec v0.1

Conversational analytics: user asks in natural language, agent queries the warehouse through Cortex (the MCP server), selects a chart, front-end renders a declarative spec. Pinned widgets become reusable artifacts with permission-aware cache.

## Components

| Component | Role | Owns |
|-----------|------|------|
| Agent (OpenCode harness) | Orchestrator | Intent parse, Cortex tool calls, compose widget specs |
| Cortex (MCP server) | Data + artifact gateway | SQL execution, RLS/table ACL, cache, artifact store |
| Chart component | Visualization advisor | Map data shape → chart type + encoding |
| Front-end dashboard | Renderer | Render spec, pin/share UI, freshness indicator |

## Request flow

1. User: "How many meetings yesterday, trend last 30 days, month to date."
2. Agent splits into three intents (point, time series, aggregate).
3. Agent calls Cortex query tool once per intent.
4. Cortex checks table + row permissions for the caller. Cache key = `sha256(normalized_sql) + role`.
5. Chart component emits a declarative spec (not pixels): `kpi_card` | `line` | `bar`.
6. Front-end renders with existing libraries.
7. Pin → Cortex saves artifact `{widget_id, chart_type, sql, spec, owner, shared_with}`.
8. Similar question from another authorized user → fingerprint match → cache hit; Cortex still re-checks ACL before serve.

## Data contracts

### Agent → front-end (`DeclarativeChartSpec`)

```json
{
  "widget_id": "w_meetings_30d_trend",
  "chart_type": "line",
  "title": "Meetings — last 30 days",
  "encoding": { "x": "date", "y": "count" },
  "data": { "rows": [{"date": "2026-09-01", "count": 30}] },
  "source": "cache | warehouse",
  "fingerprint": "0496a27faa17",
  "freshness": "2026-09-25T10:53:00+05:30"
}
```

### Artifact (`PinnedWidget`)

```json
{
  "widget_id": "w-trend-001",
  "chart_type": "line",
  "sql": "SELECT date, COUNT(*) FROM meetings WHERE date >= CURRENT_DATE - 30 GROUP BY date",
  "spec": {},
  "owner": "alice",
  "shared_with": ["bob"],
  "created_at": "2026-09-25T10:53:00+05:30"
}
```

## Permissions

Cortex is the only enforcement point. Cache is keyed by role so two roles never share a result set. Artifact retrieve checks `owner == user OR user in shared_with` **and** table ACL.

## Open questions

- Cache TTL for "yesterday" queries (goes stale at midnight).
- Intent match: exact SQL fingerprint vs semantic similarity.
- Refresh policy: on view vs scheduled.

## Non-goals (v0.1)

- Agent-written SQL without a schema tool.
- Cross-warehouse joins.
- Write queries.
