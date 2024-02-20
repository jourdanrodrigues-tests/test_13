import os

from core.settings._environment import BASE_DIR

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "assets", "media")

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "assets", "static")
