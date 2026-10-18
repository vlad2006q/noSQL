# Redis Session Store — вариант 9

Учебный проект: хранение пользовательских сессий в Redis с использованием **Redis Hash** и автоматического истечения срока действия (**TTL/EXPIRE**).

## Возможности
- создание сессии с TTL;
- получение данных сессии и проверка активности;
- продление TTL;
- обновление полей сессии;
- завершение сессии пользователем (logout);
- принудительный отзыв сессии (revoke);
- демонстрация 30 синтетических сессий;
- автоматические тесты на `fakeredis`, не требующие работающего Redis.

## Требования
- Python 3.10 или новее;
- Redis Server для запуска демонстрационных скриптов;
- Windows + VS Code подходит.

## Установка на Windows
Открой папку проекта в VS Code. В терминале PowerShell выполни:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

### Запуск Redis без Docker
Один из вариантов — WSL Ubuntu. В PowerShell от имени администратора:

```powershell
wsl --install -d Ubuntu
```

После установки открой Ubuntu и выполни:

```bash
sudo apt update
sudo apt install redis-server -y
sudo service redis-server start
redis-cli ping
```

Ожидаемый ответ: `PONG`. Если Redis доступен на `localhost:6379`, проект можно запускать из PowerShell. Если соединение не проходит, запускай проект и Redis внутри WSL либо настрой подключение согласно своей среде.

## Запуск
Из корневой папки проекта:

```powershell
.\.venv\Scripts\python.exe scripts\seed.py
.\.venv\Scripts\python.exe scripts\demo_queries.py
.\.venv\Scripts\python.exe src\main.py
```

Интерактивное меню позволяет создавать, просматривать, продлевать и завершать сессии.

## Тесты
Тесты используют `fakeredis`, поэтому для них не требуется отдельный Redis Server:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

## Структура
```text
redis-session-project/
├── src/session_store.py   # слой доступа к Redis
├── src/main.py            # консольное меню
├── scripts/seed.py        # создание 30 тестовых сессий
├── scripts/demo_queries.py# демонстрация сценариев доступа
├── tests/                 # автоматические тесты
├── docs/ADR.md            # архитектурное решение
├── docs/architecture.mmd  # диаграмма Mermaid
├── docs/report.pdf        # учебный отчёт
└── docs/presentation.pptx # презентация на 9 слайдов
```

## Перед сдачей
1. Впиши свои ФИО, группу, дисциплину и преподавателя в титульные поля отчёта/презентации, если это требуется.
2. Запусти тесты и демо, сделай собственные скриншоты работающей программы.
3. Убедись, что Redis доступен для `seed.py`, `demo_queries.py` и `main.py`.
4. Не загружай `.env` с секретами. В репозитории оставляй только `.env.example`.

## Примечание
Это учебная демонстрация. Для production-системы нужны HTTPS, защищённые cookie, CSRF-защита, ротация session ID, ограничения доступа к Redis, мониторинг и дополнительные меры против фиксации/кражи сессии.
