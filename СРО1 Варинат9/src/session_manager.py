import redis,os
from dotenv import load_dotenv
load_dotenv()
r=redis.Redis(host=os.getenv("REDIS_HOST"),port=int(os.getenv("REDIS_PORT")),db=int(os.getenv("REDIS_DB")),decode_responses=True)
class SessionManager:
    def create_session(self,sid,uid,role):
        r.hset(f"session:{sid}",mapping={"user_id":uid,"role":role,"status":"active"});r.expire(f"session:{sid}",3600)
    def get_session(self,sid): return r.hgetall(f"session:{sid}")
    def update_session(self,sid,role): r.hset(f"session:{sid}","role",role)
    def delete_session(self,sid): r.delete(f"session:{sid}")
