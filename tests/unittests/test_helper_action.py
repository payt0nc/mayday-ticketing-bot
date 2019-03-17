import unittest
import pytest
import mongomock

from mayday.controllers.mongo import MongoController
from mayday.helpers.action_helper import ActionHelper
from mayday.objects import User, Action


USER_ID = 123456789
USERNAME = 'testcase'


@pytest.mark.usefixtures()
class Test(unittest.TestCase):

    @pytest.fixture(autouse=True, scope='function')
    def before_all(self):
        client = mongomock.MongoClient()
        self.mongo = MongoController(mongo_client=client)
        self.helper = ActionHelper(mongo_controller=self.mongo)

    def test_save_action(self):

        action = Action(USER_ID, USERNAME)
        assert self.helper.save_current_action(action)

        action_in_cache = self.helper.load_last_action(USER_ID, USERNAME)
        assert action.user_id == action_in_cache.user_id
        assert action.username == action_in_cache.username
        assert action.action_module_name == action_in_cache.action_module_name
        assert action.field_name == action_in_cache.field_name
        assert action.field_value == action_in_cache.field_value

    def test_update_action(self):
        action = Action(USER_ID, USERNAME)
        assert self.helper.save_current_action(action)

        action = self.helper.load_last_action(USER_ID, USERNAME)
        action.action_module_name = 'search_tickets'
        assert self.helper.save_current_action(action)

        updated_action = self.helper.load_last_action(USER_ID, USERNAME, action_module_name='search_tickets')
        assert action.user_id == updated_action.user_id
        assert action.username == updated_action.username
        assert action.action_module_name == updated_action.action_module_name
        assert action.field_name == updated_action.field_name
        assert action.field_value == updated_action.field_value
