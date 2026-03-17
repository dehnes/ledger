# src/core/settings/production.py
from .base import *
import os

DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY")
ALLOWED_HOSTS = ["yourdomain.com"]

# Force SSL, secure cookies, etc.
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
