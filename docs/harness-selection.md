# Harness selection: lightweight agent harnesses

Context: a single agent that parses intent, calls Cortex (MCP) tools, and emits a JSON chart spec. Not a coding agent — no sandboxing or filesystem editing needed.

## Shortlist

| Harness | License | Why it fits |
|---|---|---|
| **OpenCode** (chosen) | MIT | Model-agnostic (75+ providers), strong MCP support, TUI + desktop + IDE. No vendor lock-in. |
| smolagents | Apache 2.0 | Most minimal (~1,000 lines). Code-as-action: agent writes Python instead of JSON tool calls — nice for composing Cortex queries. |
| OpenAI Agents SDK | (vendor) | Provider-agnostic across 100+ models, built-in tracing and guardrails, added sandboxing + long-horizon support in 2026. Fastest path from zero to working. |
| Pi | MIT | Context discipline under 1,000-token system prompt; topped Databricks cost-per-task at equal quality. |
| opencode | MIT | Same project as OpenCode (formerly sst/opencode, transferred to anomalyco). |

## Ruled out

- **Claude Code** — proprietary, Anthropic-only, terminal-coding oriented. Overkill and lock-in.
- **Codex CLI** — OpenAI-first, sandbox-first. Built for repo editing, not tool-calling analytics loops. (Not to be confused with Cortex, our MCP server.)
- **LangGraph** — powerful but steep; explicit graph modeling is more than this linear tool loop needs.
- **CrewAI** — role-based multi-agent crews; unnecessary orchestration for one agent.

## Decision

OpenCode. It gives the Claude Code / Codex loop experience without model lock-in, and its MCP integration maps directly onto Cortex, the existing MCP server that already enforces ACL and caching.

See `docs/architecture.md` for the full diagram.
