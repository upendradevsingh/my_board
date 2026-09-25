"""NL-to-dashboard agent — console prototype.

Run: python prototype.py
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any


def fingerprint(sql: str) -> str:
    return hashlib.sha256(sql.strip().lower().encode()).hexdigest()[:12]


@dataclass
class User:
    name: str
    role: str


ACL = {
    "analyst": {"meetings"},
    "viewer": set(),
}

INTENTS = {
    "yesterday": {
        "label": "Meetings yesterday",
        "type": "point",
        "table": "meetings",
        "sql": "SELECT COUNT(*) AS count FROM meetings WHERE date = CURRENT_DATE - 1",
        "data": {"count": 42},
    },
    "trend": {
        "label": "Meetings last 30 days",
        "type": "trend",
        "table": "meetings",
        "sql": "SELECT date, COUNT(*) AS count FROM meetings WHERE date >= CURRENT_DATE - 30 GROUP BY date",
        "data": {"series": [30, 33, 35, 38, 40, 42]},
    },
    "mtd": {
        "label": "Meetings month to date",
        "type": "aggregate",
        "table": "meetings",
        "sql": "SELECT COUNT(*) AS count FROM meetings WHERE date >= DATE_TRUNC('month', CURRENT_DATE)",
        "data": {"count": 310},
    },
}


def chart_for(intent: dict) -> dict:
    t = intent["type"]
    if t == "point":
        return {"chart_type": "kpi_card", "value": intent["data"]["count"]}
    if t == "trend":
        return {"chart_type": "line", "series": intent["data"]["series"], "x": "date", "y": "count"}
    if t == "aggregate":
        return {"chart_type": "bar", "value": intent["data"]["count"]}
    return {"chart_type": "table", "data": intent["data"]}


class MCPServer:
    def __init__(self) -> None:
        self.cache: dict[tuple[str, str], Any] = {}
        self.artifacts: dict[str, dict] = {}

    def query(self, sql: str, table: str, user: User) -> dict:
        if table not in ACL.get(user.role, set()):
            return {"status": "permission_denied", "user": user.name, "table": table}
        fp = fingerprint(sql)
        key = (fp, user.role)
        if key in self.cache:
            return {"status": "cache", "fingerprint": fp, "data": self.cache[key]}
        return {"status": "fresh", "fingerprint": fp, "data": None}

    def put_cache(self, sql: str, role: str, data: Any) -> None:
        self.cache[(fingerprint(sql), role)] = data

    def save_artifact(self, widget_id: str, chart_type: str, sql: str, spec: dict, owner: str) -> dict:
        art = {
            "widget_id": widget_id,
            "chart_type": chart_type,
            "sql": sql,
            "spec": spec,
            "owner": owner,
            "shared_with": [],
        }
        self.artifacts[widget_id] = art
        return art

    def share(self, widget_id: str, target: str) -> dict | None:
        art = self.artifacts.get(widget_id)
        if not art:
            return None
        if target not in art["shared_with"]:
            art["shared_with"].append(target)
        return art

    def get_artifact(self, widget_id: str, user: User) -> dict:
        art = self.artifacts.get(widget_id)
        if not art:
            return {"status": "not_found"}
        if art["owner"] == user.name or user.name in art["shared_with"]:
            return art
        return {"status": "permission_denied", "user": user.name}


class Agent:
    def __init__(self, mcp: MCPServer) -> None:
        self.mcp = mcp

    def parse(self, text: str) -> list[str]:
        t = text.lower()
        keys = []
        if "yesterday" in t:
            keys.append("yesterday")
        if "30" in t or "trend" in t:
            keys.append("trend")
        if "month" in t or "mtd" in t:
            keys.append("mtd")
        return keys or ["yesterday"]

    def handle(self, text: str, user: User) -> list[dict]:
        widgets = []
        for key in self.parse(text):
            intent = INTENTS[key]
            res = self.mcp.query(intent["sql"], intent["table"], user)
            if res["status"] == "permission_denied":
                widgets.append({"intent": key, "error": res})
                continue
            if res["status"] == "fresh":
                self.mcp.put_cache(intent["sql"], user.role, intent["data"])
                data = intent["data"]
            else:
                data = res["data"]
            spec = chart_for({**intent, "data": data})
            widgets.append(
                {
                    "widget_id": f"w_{key}",
                    "title": intent["label"],
                    "status": res["status"],
                    "fingerprint": fingerprint(intent["sql"]),
                    "spec": spec,
                    "sql": intent["sql"],
                }
            )
        return widgets


def demo() -> None:
    mcp = MCPServer()
    agent = Agent(mcp)
    alice, bob, carol = User("alice", "analyst"), User("bob", "analyst"), User("carol", "viewer")

    print("=== Alice asks all three ===")
    w = agent.handle(
        "how many meetings yesterday, trend last 30 days, month to date", alice
    )
    print(json.dumps(w, indent=2))

    print("\n=== Alice pins trend ===")
    trend = next(x for x in w if x["widget_id"] == "w_trend")
    print(json.dumps(mcp.save_artifact("w_trend", trend["spec"]["chart_type"], trend["sql"], trend["spec"], "alice"), indent=2))

    print("\n=== Bob asks trend (cache hit, same role) ===")
    print(json.dumps(agent.handle("meeting trend last 30 days", bob), indent=2))

    print("\n=== Carol asks (denied) ===")
    print(json.dumps(agent.handle("meetings yesterday", carol), indent=2))

    print("\n=== Share with Bob, Carol still blocked ===")
    mcp.share("w_trend", "bob")
    print("bob:", json.dumps(mcp.get_artifact("w_trend", bob), indent=2))
    print("carol:", json.dumps(mcp.get_artifact("w_trend", carol), indent=2))


if __name__ == "__main__":
    demo()
