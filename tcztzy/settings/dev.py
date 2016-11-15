from .common import *  # noqa

DEBUG = True

ALLOWED_HOSTS = ['blog', '127.0.0.1']

STATIC_ROOT = str(DATA_DIR.joinpath('static_root'))
