from flask import Response

from my_site.data.users import User
from viewmodels.account.register_viewmodel import RegisterViewModel
from tests.test_client import flask_app, client
import unittest.mock

def test_example():
    print("Test example...")
    assert 1 + 2 == 3


def test_register_validation_when_valid():
    # Arrange
    form_data = {
        'name': 'Ruchti',
        'email': 't@g.com',
        'password': 'abc'*6
    }

    with flask_app.test_request_context(path='/account/register', data=form_data):
        vm = RegisterViewModel()
    # Act
    target = 'services.user_service.find_user_by_email'
    with unittest.mock.patch(target, return_value=None):
        vm.validate()

    # Assert
    assert vm.error is None


def test_register_validation_for_existing_user():
    # Arrange
    form_data = {
        'name': 'Ruchti',
        'email': 't@g.com',
        'password': 'abc'*6
    }

    with flask_app.test_request_context(path='/account/register', data=form_data):
        vm = RegisterViewModel()
    # Act
    target = 'services.user_service.find_user_by_email'
    test_user = User(email=form_data.get('email'))
    with unittest.mock.patch(target, return_value=test_user):
        vm.validate()

    # Assert
    assert vm.error is not None
    assert 'already exists' in vm.error


def test_register_view_new_user():
    # Arrange
    from views.account_views import register_post
    form_data = {
        'name': 'Ruchti',
        'email': 't@g.com',
        'password': 'abc'*6
    }

    target = 'services.user_service.find_user_by_email'
    find_user = unittest.mock.patch(target, return_value=None)
    target = 'services.user_service.create_user'
    create_user = unittest.mock.patch(target, return_value=User())
    request = flask_app.test_request_context(path='/account/register', data=form_data)
    with find_user, create_user, request:
        # Act
        resp: Response = register_post()

    # Assert
    assert resp.location == '/account'


def test_int_account_home_no_login(client):
    target = 'services.user_service.find_user_by_id'
    with unittest.mock.patch(target, return_value=None):
        resp: Response = client.get('/account')

    assert resp.status_code == 302
    assert resp.location == 'http://localhost/account/login'


def test_int_account_home_with_login(client):
    target = 'services.user_service.find_user_by_id'
    test_user = User(name='Ruchti', email='t@g.com')
    with unittest.mock.patch(target, return_value=test_user):
        resp: Response = client.get('/account')

    assert resp.status_code == 200
    assert b'Ruchti' in resp.data