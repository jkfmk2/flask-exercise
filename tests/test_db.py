def test_user_exists(user, post):
    assert user.username == 'tester'
    assert post.title == 'test title'