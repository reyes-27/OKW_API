from .base import BASE_DIR, INSTALLED_APPS, MIDDLEWARE, env
import os

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'backend']

INSTALLED_APPS.append("debug_toolbar")

MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

INTERNAL_IPS = [
    "0.0.0.0",
]

MEDIA_ROOT = os.path.join(BASE_DIR / "media")
MEDIA_URL = "/media/"

DATABASES = {
    'default': {
        'ENGINE': env.str('SQL_ENGINE'),
        'NAME': env.str('SQL_NAME'),
        'USER': env.str('SQL_USER'),
        'PASSWORD': env.str('SQL_PASSWORD'),
        'HOST': env.str('SQL_HOST'),
        'PORT': env.str('SQL_PORT'),
    }
}


# DATABASES = {
#     'default': dj_database_url.config(
#         default = env.str("DATABASE_URL"),
#         conn_max_age = 600,
#     )
# }