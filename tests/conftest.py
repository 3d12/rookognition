#Rookognition - A web-based chess vision exercise.
#Copyright (C) 2025 Nick Edner

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published
#by the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.

#You should have received a copy of the GNU Affero General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os
import tempfile

import pytest
from rookognition import create_app

#with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
#    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app_with_no_data():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        })

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def app(app_with_no_data):
    #with app_with_no_data.app_context():
    #    get_db().executescript(_data_sql)
    return app_with_no_data

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

#class AuthActions(object):
#    def __init__(self, client):
#        self._client = client
#
#    def login(self, username='test', password='test'):
#        return self._client.post(
#                '/auth/login',
#                data={'username': username, 'password': password}
#                )
#
#    def logout(self):
#        return self._client.get('/auth/logout')

#@pytest.fixture
#def auth(client):
#    return AuthActions(client)
