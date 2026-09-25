# UI requirements — dashboard + chat canvas

Dashboard-first. Conversation on the right. **Widgets render only on the left artifact canvas**, never as HTML inside the thread.

## Chat vs canvas

| Surface | Renders |
|---|---|
| Right thread | Text, status, artifact chips |
| Left canvas | KPI / line / bar from JSON spec |
| Home dashboard | Pinned copies only |

Chip click focuses the matching card on the left. Pin copies the spec onto the current dashboard via Cortex.

Prototype: `app.html`
