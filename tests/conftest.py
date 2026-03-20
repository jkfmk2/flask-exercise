import os
import pytest
from flaskr import create_app
from flaskr.extensions import db
from flaskr.models import User

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def session(app):
    yield db.session
    db.session.rollback()

@pytest.fixture
def user(session):
    user = User(username='tester')
    user.password = '#1234Abc'
    session.add(user)
    session.commit()
    return user

@pytest.fixture
def other_user(session):
    user = User(username='others')
    user.password = '#1234Abc'
    session.add(user)
    session.commit()
    return user

@pytest.fixture
def post(session, user):
    from flaskr.models import Post
    post = Post(
        title='test title',
        body='test body',
        author_id=user.id
    )
    session.add(post)
    session.commit()
    return post

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def register(self, username='tester123', password='#1234Abc', confirm_password='#1234Abc'):
        return self._client.post(
            '/auth/register',
            data = {
                'username': username,
                'password': password,
                'confirm_password': confirm_password
            }
        )
    
    def login(self, username='tester', password='#1234Abc'):
        return self._client.post(
            '/auth/login',
            data = {'username': username, 'password': password}
        )
    
    def logout(self):
        return self._client.get('/auth/logout')
    
@pytest.fixture
def auth(client, user, other_user):
    return AuthActions(client)
