# UI requirements — dashboard + chat canvas

**Product:** NL-to-Dashboard (OpenCode agent + Cortex MCP)
**Pattern:** Dashboard-first. Chat is a right-hand canvas, not a chatbot home.

Claude and ChatGPT put chat left and artifacts right. This product inverts that: the **board is the work**, the conversation is a copilot docked on the **right**.

## Information architecture

```
App
├── Home (default) — user's main dashboard
├── Dashboards (list + create)
├── Chat canvas (split on current board)
└── Settings
```

Chrome: top bar (burger, title, user), bottom-right chat FAB, left drawer.

## Screens

### S1 Home
User lands on their main dashboard, full width. Pinned widgets or empty state. Chat FAB. Burger.
Do not open on a blank chat.

### S2 Drawer
280px slide-over: dashboard list, New dashboard, Settings. Esc / scrim closes.

### S3 Chat canvas
Left ~60% live visualization. Right ~40% conversation + composer.
Close returns to S1; pinned widgets stay on the board.
Mobile: conversation full-bleed.

### S4 Create dashboard
Modal: name required. New empty board becomes current.

### S5 Settings
Display name, default board, theme, Cortex connection.

## Wireframes

S1:
```
[ ☰  Main                    Alice ]
[ KPI ] [ KPI ] [ KPI ]
[ area chart ]
                                 (chat)
```

S3:
```
[ live board / artifacts ] | [ thread          ]
                           | [ composer        ]
```

## Interaction requirements

- UX-01 First paint is main dashboard.
- UX-02 Chat from persistent bottom-right control.
- UX-03 Opening chat splits the page; does not destroy the board.
- UX-04 Conversation on the right; visualization on the left.
- UX-05 Agent output is widgets (JSON specs), not markdown-only.
- UX-06 Pin writes an artifact to the current dashboard via Cortex.
- UX-07 Burger lists dashboards the user can open.
- UX-08 Create dashboard is one modal.
- UX-09 Esc closes drawer, modal, or chat.
- UX-10 Mobile: chat full-bleed.
- UX-11 FAB hidden while chat is open.
- UX-12 Closing chat keeps newly pinned widgets.

Prototype: `app.html`
