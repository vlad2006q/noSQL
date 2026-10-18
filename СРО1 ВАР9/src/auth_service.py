from session_manager import SessionManager
sm=SessionManager()
def login(uid): sm.create_session(f"user{uid}",uid,"student")
def logout(uid): sm.delete_session(f"user{uid}")
def refresh(uid): pass
