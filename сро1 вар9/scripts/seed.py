import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dotenv import load_dotenv
import redis
from src.session_store import SessionStore
load_dotenv()
r = redis.Redis(host=os.getenv('REDIS_HOST','localhost'), port=int(os.getenv('REDIS_PORT','6379')),
                db=int(os.getenv('REDIS_DB','0')), decode_responses=True)
r.ping()
store = SessionStore(r, int(os.getenv('SESSION_TTL','1800')))
for i in range(1,31):
    sid = store.create_session(f'student_{i:02d}', {'role':'student','source':'seed'}, ttl=1800 + i*10)
    print(f'{i:02d}. student_{i:02d} -> {sid}')
print('Готово: создано 30 синтетических сессий.')
