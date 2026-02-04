import os
import shelve
import time

RATE_LIMIT_PER_MINUTE = os.getenv('RATE_LIMIT_PER_MINUTE', 60)
RATE_LIMIT_DB = 'local_rate_limit.db'


class LocalRateLimiter():        

    @staticmethod
    def _key(user_id: str) -> str:
        return f'rate_limit_user_id:{user_id}'
    

    def allow_request(self, user_id: str) -> bool:
        now = int(time.time())
        window = now // 60  # a minute window
        key = self._key(user_id)
        with shelve.open(RATE_LIMIT_DB, writeback=True) as db:
            entry = db.get(key, {"window": window, "count": 0})
            if entry["window"] != window:
                entry["window"] = window
                entry["count"] = 0
            if entry["count"] + 1 > RATE_LIMIT_PER_MINUTE:
                db[key] = entry
                return False
            entry["count"] += 1
            db[key] = entry
            return True
        return False
    