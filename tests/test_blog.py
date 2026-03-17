import pytest
from flaskr.models import Post

def test_index(client, auth, post):
    response = client.get('/')
    assert response.status_code == 200
    assert b'test title' in response.data

    auth.login()
    response = client.get('/')
    with client.session_transaction() as session:
        assert session['_user_id'] == '1'

@pytest.mark.parametrize('path',(
        '/create',
        '1/update',
        '1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.status_code == 302
    redirect_url = response.headers['Location']
    next_response = client.get(redirect_url)
    assert b'Please log in to access this page.' in next_response.data

@pytest.mark.parametrize('path', (
        '/2/update',
        '/2/delete'
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404

def test_create_post(auth, client, app):
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'title': 'new post', 'body': 'content'})
    with app.app_context():
         post = Post.query.filter_by(title='new post').first()
         assert post is not None

def test_update_post(app, client, auth, post):
    auth.login()
    assert client.get('/1/update').status_code == 200 
    client.post('/1/update', data={'title': 'updated', 'body': 'new body'})
    with app.app_context():
        post = Post.query.get(post.id)
        assert post.title == 'updated'

def test_delete_post(auth, client, app, post):
    auth.login()
    with app.app_context():
        post = Post.query.filter_by(title='test title').first()
        assert post.title == 'test title'
    response = client.post('/1/delete')
    assert response.headers['Location'] == '/'
    with app.app_context():
        post = Post.query.filter_by(title='test title').first()
        assert post is None

def test_author_required(client, auth, post):
    auth.login(username='others', password='#1234Abc')
    response = client.get('/')
    with client.session_transaction() as session:
        assert session['_user_id'] == '2'

    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403

