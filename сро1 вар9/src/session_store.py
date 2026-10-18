"""Redis-backed session storage for the coursework demo."""
from __future__ import annotations
import secrets
import time
from typing import Optional, Dict, Any
import redis

class SessionStore:
    def __init__(self, client: redis.Redis, default_ttl: int = 1800, prefix: str = "session:"):
        if default_ttl <= 0:
            raise ValueError("default_ttl must be positive")
        self.client = client
        self.default_ttl = int(default_ttl)
        self.prefix = prefix

    def _key(self, session_id: str) -> str:
        return f"{self.prefix}{session_id}"

    def create_session(self, user_id: str, metadata: Optional[Dict[str, Any]] = None, ttl: Optional[int] = None) -> str:
        if not user_id.strip():
            raise ValueError("user_id cannot be empty")
        lifetime = int(ttl or self.default_ttl)
        if lifetime <= 0:
            raise ValueError("ttl must be positive")
        session_id = secrets.token_urlsafe(24)
        now = int(time.time())
        fields = {"session_id": session_id, "user_id": user_id, "created_at": str(now),
                  "last_seen": str(now), "metadata": str(metadata or {})}
        pipe = self.client.pipeline(transaction=True)
        pipe.hset(self._key(session_id), mapping=fields)
        pipe.expire(self._key(session_id), lifetime)
        pipe.execute()
        return session_id

    def get_session(self, session_id: str) -> Optional[dict]:
        data = self.client.hgetall(self._key(session_id))
        if not data:
            return None
        return data

    def is_active(self, session_id: str) -> bool:
        return bool(self.client.exists(self._key(session_id)))

    def get_ttl(self, session_id: str) -> int:
        """Return seconds remaining; Redis returns -2 if absent and -1 if no TTL."""
        return int(self.client.ttl(self._key(session_id)))

    def touch(self, session_id: str, ttl: Optional[int] = None) -> bool:
        key = self._key(session_id)
        if not self.client.exists(key):
            return False
        lifetime = int(ttl or self.default_ttl)
        if lifetime <= 0:
            raise ValueError("ttl must be positive")
        self.client.hset(key, "last_seen", str(int(time.time())))
        return bool(self.client.expire(key, lifetime))

    def update_session(self, session_id: str, fields: Dict[str, Any]) -> bool:
        key = self._key(session_id)
        if not fields or not self.client.exists(key):
            return False
        safe = {str(k): str(v) for k, v in fields.items() if k not in {"session_id", "user_id", "created_at"}}
        if not safe:
            return False
        self.client.hset(key, mapping=safe)
        return True

    def logout(self, session_id: str) -> bool:
        return bool(self.client.delete(self._key(session_id)))

    def revoke_session(self, session_id: str) -> bool:
        """Administrative revocation; intentionally equivalent to deletion."""
        return self.logout(session_id)

    def list_sessions(self, user_id: Optional[str] = None) -> list[dict]:
        result = []
        for key in self.client.scan_iter(match=f"{self.prefix}*"):
            item = self.client.hgetall(key)
            if item and (user_id is None or item.get("user_id") == user_id):
                result.append(item)
        return result
