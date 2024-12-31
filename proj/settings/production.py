from .base import *

DEBUG = False
CSRF_TRUSTED_ORIGINS = ["https://contour.mugboy.dev"]

try:
    from .local import *
except ImportError:
    pass
