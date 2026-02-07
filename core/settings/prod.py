import dj_database_url
from .base import env

DATABASES = {
    'default': dj_database_url.config(
        default = env.str("DATABASE_URL"),
        conn_max_age = 600,
    )
}