"""Shared Selenium Grid session cleanup for QA browser startup."""
from ..logger import get_logger

log = get_logger("browser.grid")


def cleanup_grid_sessions(grid_url: str, *, owned_session_ids=()) -> None:
    """仅清理调用方明确拥有的 session；默认不查询或改变共享 Grid。"""
    import json
    import urllib.request
    from urllib.parse import quote
    owned = set(owned_session_ids)
    if not owned:
        return
    try:
        status_url = grid_url.rstrip("/") + "/status"
        with urllib.request.urlopen(status_url, timeout=5) as resp:
            data = json.loads(resp.read())
        nodes = data.get("value", {}).get("nodes", [])
        for node in nodes:
            for slot in node.get("slots", []):
                session = slot.get("session")
                if session and session.get("sessionId") in owned:
                    sid = session["sessionId"]
                    log.info("清理残留 session: %s", sid)
                    delete_url = grid_url.rstrip("/") + "/session/" + quote(sid, safe="")
                    req = urllib.request.Request(delete_url, method="DELETE")
                    try:
                        with urllib.request.urlopen(req, timeout=5):
                            pass
                    except Exception:
                        pass
    except Exception as e:
        log.debug("Grid 清理跳过: %s", e)
