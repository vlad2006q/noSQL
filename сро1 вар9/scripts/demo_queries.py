import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dotenv import load_dotenv
import redis
from src.session_store import SessionStore
load_dotenv()
r = redis.Redis(host=os.getenv('REDIS_HOST','localhost'), port=int(os.getenv('REDIS_PORT','6379')),
                db=int(os.getenv('REDIS_DB','0')), decode_responses=True)
r.ping(); store = SessionStore(r, int(os.getenv('SESSION_TTL','1800')))
print('\n1) Создание сессии')
sid = store.create_session('demo_user', {'role':'tester'})
print('session_id:', sid)
print('\n2) Чтение Hash:', store.get_session(sid))
print('\n3) Проверка существования:', store.is_active(sid))
print('\n4) Остаток TTL:', store.get_ttl(sid))
print('\n5) Продление TTL:', store.touch(sid, 2400))
print('\n6) TTL после продления:', store.get_ttl(sid))
print('\n7) Обновление last_seen/поля:', store.update_session(sid, {'ip':'192.0.2.10'}))
print('\n8) Получение сессий demo_user:', store.list_sessions('demo_user'))
print('\n9) Поиск всех сессий (демонстрация SCAN):', len(store.list_sessions()))
print('\n10) Завершение сессии:', store.logout(sid))
print('После logout активна:', store.is_active(sid), 'TTL:', store.get_ttl(sid))
