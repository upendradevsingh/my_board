# NL-to-Dashboard Agent

Architecture spec and interactive prototype for a conversational analytics path:

warehouse → MCP (ACL + cache + artifacts) → chart spec → existing front-end renderer → pin/share.

## Files

- `SPEC.md` — components, flow, contracts, open questions
- `prototype.html` — interactive demo styled after shadcn/ui dashboard-01: sidebar shell, site header, section cards, area chart, light/dark theme
- `prototype.py` — same logic as a console script

## Try the prototype

Download `prototype.html` and open it in a browser.

1. Stay as Alice. Click **All three** then **Run**. You get KPI cards plus a trend area chart. First pass is `fresh`.
2. Run the 30-day trend again — badge flips to `cached`.
3. **Pin to dashboard**, then **Share with Bob**.
4. Switch user to Bob → artifact is loadable. Same question is a cache hit.
5. Switch to Carol → meetings queries and the shared widget are denied.
6. Use the sun icon in the header to toggle dark mode.

## Design rules this demo encodes

- Chart component emits a spec, not pixels.
- Cache key is `fingerprint(sql) + role`, not user name alone.
- MCP re-checks table ACL on cache hits and on artifact load.
- Artifact visibility is owner or `shared_with`, plus table ACL.
