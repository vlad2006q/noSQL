from redis_client import client
class SessionManager:
 def create_session(self,sid,uid,role):
  client.hset(f"session:{sid}",mapping={"user_id":uid,"role":role,"status":"active"})
  client.expire(f"session:{sid}",3600)
 def get_session(self,sid): return client.hgetall(f"session:{sid}")
 def update_role(self,sid,role): client.hset(f"session:{sid}","role",role)
 def delete_session(self,sid): client.delete(f"session:{sid}")
 def exists(self,sid): return client.exists(f"session:{sid}")
 def ttl(self,sid): return client.ttl(f"session:{sid}")
