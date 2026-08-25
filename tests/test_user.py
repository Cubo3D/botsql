from services import create_user, get_user


def test_create_user():
    name = "user_test"
    id = 12345
    user = create_user(name, id)

    assert user is not None
    assert user.userid == id
    assert user.username == name


def test_get_user():
    name = "user_test2"
    id = 123

    create_user(name, id)
    user = get_user(id)

    assert user is not None
    assert user.username == name
    assert user.userid == id
