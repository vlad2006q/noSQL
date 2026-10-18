"""Small interactive console for the Redis session store."""
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dotenv import load_dotenv
import redis
from src.session_store import SessionStore

load_dotenv()
client = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=int(os.getenv("REDIS_PORT", "6379")),
                     db=int(os.getenv("REDIS_DB", "0")), decode_responses=True, socket_connect_timeout=3)
store = SessionStore(client, int(os.getenv("SESSION_TTL", "1800")))

def main():
    try:
        client.ping()
    except redis.RedisError as exc:
        print(f"Не удалось подключиться к Redis: {exc}\nПроверь Redis Server и настройки .env.")
        return
    while True:
        print("\n=== Redis Session Store ===\n1. Создать сессию\n2. Показать сессию\n3. Проверить активность/TTL\n4. Продлить сессию\n5. Обновить поле\n6. Logout (удалить)\n7. Список сессий пользователя\n0. Выход")
        choice = input("Выбор: ").strip()
        if choice == "0": break
        if choice == "1":
            uid = input("user_id: ").strip()
            sid = store.create_session(uid)
            print("Создана сессия ID:", sid)
        elif choice == "2":
            sid = input("session_id: ").strip(); print(store.get_session(sid) or "Сессия не найдена/истекла")
        elif choice == "3":
            sid = input("session_id: ").strip(); print("Активна:", store.is_active(sid), "TTL:", store.get_ttl(sid), "сек.")
        elif choice == "4":
            sid = input("session_id: ").strip(); print("Продлено" if store.touch(sid) else "Сессия не найдена")
        elif choice == "5":
            sid = input("session_id: ").strip(); field = input("Имя поля: ").strip(); value = input("Значение: ")
            print("Обновлено" if store.update_session(sid, {field: value}) else "Не удалось обновить")
        elif choice == "6":
            sid = input("session_id: ").strip(); print("Сессия завершена" if store.logout(sid) else "Сессия не найдена")
        elif choice == "7":
            uid = input("user_id: ").strip(); print(*store.list_sessions(uid), sep="\n")
        else: print("Неизвестный пункт меню")

if __name__ == "__main__": main()
