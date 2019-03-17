import time


class Action:

    def __init__(self, user_id: int, username: str):
        self._user_id = user_id
        self._username = username

        self._action_module_name = ''
        self._field_name = ''
        self._field_value = None

        self._updated_at = int(time.time())
        self._object_id = ''

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def username(self) -> str:
        return self._username

    @property
    def action_module_name(self) -> str:
        return self._action_module_name

    @action_module_name.setter
    def action_module_name(self, value: str):
        self._action_module_name = value

    @property
    def field_name(self) -> str:
        return self._field_name

    @field_name.setter
    def field_name(self, value: str):
        self._field_name = value

    @property
    def field_value(self) -> str:
        return self._field_value

    @field_value.setter
    def field_value(self, value: str):
        self._field_value = value

    @property
    def object_id(self) -> str:
        return self._object_id

    @property
    def updated_at(self) -> int:
        self._updated_at = int(time.time())
        return self._updated_at

    def to_dict(self) -> dict:
        result = dict()
        for key, value in self.__dict__.items():
            result[key[1:]] = value
        return result

    def to_obj(self, action: dict):
        for key, value in action.items():
            if key == '_id':
                key, value = 'object_id', str(value)
            self.__setattr__('_{}'.format(key), value)
        return self

    def validate(self) -> bool:
        # validate every field value
        pass
