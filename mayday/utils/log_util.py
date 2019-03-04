import json
import time


def get_ub_log(user_id: int, username: str, funcname: str, callback_data: dict, **kwargs):
    msg = dict(
        ts=int(time.time() * 1000),
        user_id=int(user_id),
        func_name=funcname,
        username=username,
        callback_data=callback_data
    )
    if kwargs:
        msg.update(kwargs)
    return json.dumps(msg, ensure_ascii=False, sort_keys=True)
