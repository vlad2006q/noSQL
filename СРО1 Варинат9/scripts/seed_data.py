from src.session_manager import SessionManager
sm=SessionManager()
for i in range(1,31): sm.create_session(f"sess{i}",i,"student")
print("ok")