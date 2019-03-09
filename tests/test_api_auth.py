import unittest

import pytest
from mayday.controllers.request import RequestHelper
from mayday.objects import User
from requests_mock import Mocker

BASE_URL = 'mock://test.com/'


@pytest.mark.usefixtures()
class TestAuth(unittest.TestCase):

    @pytest.fixture(autouse=True, scope='function')
    def before_all(self):
        pass

    @Mocker()
    def test_auth(self, mock: Mocker):
        helper = RequestHelper(BASE_URL)
        profile = User(dict(id=123456789, username='testing_account'))
        mock.post(
            url='{}{}'.format(BASE_URL, 'auth'),
            json=dict(is_banned=False, is_admin=False),
            status_code=200
        )
        self.assertDictEqual(helper.auth(profile=profile), dict(is_banned=False, is_admin=False))
