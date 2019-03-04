def generate_user_profile(info: dict) -> dict:
    return dict(
        id=info['id'],
        username=info['username'],
        last_name=info['last_name'],
        first_name=info['first_name'],
        is_bot=info['is_bot'],
        language_code=info['language_code']
    )
