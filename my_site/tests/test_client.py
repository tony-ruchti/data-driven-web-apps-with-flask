# noinspection PyPackageRequirements
import pytest

import sys
import os

container_folder = os.path.abspath(os.path.join(
    os.path.dirname(__file__)
))
print('folder')
print(container_folder)
sys.path.insert(0, container_folder)

import my_site.app
from my_site.app import app as flask_app


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    client = flask_app.test_client()

    try:
        my_site.app.register_blueprints()
    except:
        pass

    my_site.app.setup_db()
    # client.post()

    yield client
