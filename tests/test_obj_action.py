import logging
import unittest

import pytest
from mayday.objects import Action

logger = logging.getLogger('test')

USER_ID = 123456789
USERNAME = 'testcase'


@pytest.mark.usefixtures()
class Test(unittest.TestCase):

    @pytest.fixture(autouse=True, scope='function')
    def before_all(self):
        pass

    def test_action_object_init(self):
        action = Action(USER_ID, USERNAME)
        assert action.user_id == USER_ID
        assert action.username == USERNAME
        assert action.action_module_name == ''
        assert action.field_name == ''
        assert action.field_value is None
        assert action.updated_at
        assert action.object_id == ''

    def test_action_dict_to_object(self):
        action_dict = dict(
            user_id=USER_ID,
            username=USERNAME,
            action_module_name='search',
            field_name='price',
            field_value=1
        )
        action = Action(USER_ID, USERNAME).to_obj(action_dict)
        assert action.user_id == action_dict['user_id']
        assert action.username == action_dict['username']
        assert action.action_module_name == action_dict['action_module_name']
        assert action.field_name == action_dict['field_name']
        assert action.field_value == action_dict['field_value']
