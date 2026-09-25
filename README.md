# NL-to-Dashboard Agent

Architecture spec and interactive prototype for a conversational analytics path:

warehouse → MCP (ACL + cache + artifacts) → chart spec → existing front-end renderer → pin/share.

## Files

- `SPEC.md` — components, flow, contracts, open questions
- `prototype.html` — interactive demo (switch user, ask, pin, share, ACL deny)
- `prototype.py` — same logic as a console script

## Try the prototype

Open `prototype.html` in a browser (double-click or `python -m http.server` in this folder).

1. Stay as Alice. Click **All three** then **Ask agent**. You should get a KPI, a line, and a bar. Badges say `fresh` the first time.
2. Ask the 30-day trend again — badge should flip to `cached`.
3. **Pin** the trend widget, then **Share with Bob**.
4. Switch acting user to Bob → pinned artifact is loadable. Ask the same question → cache hit.
5. Switch to Carol → ask anything about meetings → permission denied. Shared artifact stays hidden.

## Design rules this demo encodes

- Chart component emits a spec, not pixels.
- Cache key is `fingerprint(sql) + role`, not user name alone.
- MCP re-checks table ACL on cache hits and on artifact load.
- Artifact visibility is owner or `shared_with`, plus table ACL.
