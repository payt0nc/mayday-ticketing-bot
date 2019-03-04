from mayday.utils import profile_util


def auth(telegram_info: dict) -> dict:
    user_profile = profile_util.generate_user_profile(telegram_info)
    is_username_valid = bool(user_profile['username'])
    identity = _check_user_identity(user_profile)
    return dict(
        status=bool(is_username_valid and not identity['is_banned']),
        is_username_valid=is_username_valid,
        is_admin=identity['is_admin'],
        is_banned=identity['is_banned']
    )
