import fakeredis
import pytest
from src.session_store import SessionStore

@pytest.fixture
def store():
    return SessionStore(fakeredis.FakeRedis(decode_responses=True), default_ttl=60)

def test_create_and_read(store):
    sid = store.create_session('user1', {'role':'student'})
    data = store.get_session(sid)
    assert data['user_id'] == 'user1'
    assert data['session_id'] == sid

def test_ttl_is_set(store):
    sid = store.create_session('user1')
    assert 0 < store.get_ttl(sid) <= 60

def test_touch_extends_session(store):
    sid = store.create_session('user1', ttl=10)
    assert store.touch(sid, ttl=120)
    assert store.get_ttl(sid) > 10

def test_logout_removes_session(store):
    sid = store.create_session('user1')
    assert store.logout(sid)
    assert not store.is_active(sid)
    assert store.get_session(sid) is None

def test_update_existing_field(store):
    sid = store.create_session('user1')
    assert store.update_session(sid, {'ip':'192.0.2.1'})
    assert store.get_session(sid)['ip'] == '192.0.2.1'

def test_missing_session_update_returns_false(store):
    assert not store.update_session('missing-id', {'ip':'192.0.2.1'})

def test_empty_user_is_rejected(store):
    with pytest.raises(ValueError):
        store.create_session(' ')

def test_list_by_user(store):
    store.create_session('user1'); store.create_session('user2'); store.create_session('user1')
    assert len(store.list_sessions('user1')) == 2
