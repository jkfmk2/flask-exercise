import pytest
from flask import session
from flaskr.models import User

def test_register_page(client):
    response =  client.get('/auth/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_register_success(client, app):
    response = client.post(
        '/auth/register',
        data = {
            'username': 'test123',
            'password': '$ABCd1234',
            'confirm_password': '$ABCd1234',
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        user = User.query.filter_by(username='test123').first()
        assert user is not None

def test_register_redirect(auth):
    response = auth.register()
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']


def test_register_duplicate(auth):
    response = auth.register('tester', '$ABcd1345', '$ABcd1345')
    assert b'User tester is already registered.' in response.data

def test_register_password_missmatch(auth):
    response = auth.register('tester', '$ABcd1345', '$ABcd1345_wrong')
    assert b'Field must be equal to password.' in response.data

def test_login_page(client):
    response =  client.get('/auth/login')
    assert response.status_code == 200
    assert b'Log in' in response.data
    
def test_login_success(client, auth, user):
    response = auth.login()
    assert response.status_code == 302

    with client.session_transaction() as sess:
        assert sess['_user_id'] == str(user.id)

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('abcdef', '#1234Abc', b'Incorrect username.'),
    ('tester', '23232323', b'Incorrect password.' ),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()
    auth.logout()
    with client.session_transaction() as sess:
        assert '_user_id' not in sess