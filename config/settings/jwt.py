from datetime import timedelta

from config.env import env


JWT_AUTH = {
    'ACCESS_TOKEN_LIFETIME': timedelta(seconds=env.int("TTL_ACCESS_TOKEN", 900)),
    'REFRESH_TOKEN_LIFETIME': timedelta(seconds=env.int("TTL_REFRESH_TOKEN", 86400)),

    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
}
