from django.conf import settings as _settings

__author__ = 'Michael'

INTERCEPT_UNREGISTERED = False
if hasattr(_settings, 'APP_MANAGER_INTERCEPT_UNREGISTERED'):
    INTERCEPT_UNREGISTERED = _settings.APP_MANAGER_INTERCEPT_UNREGISTERED

INTERCEPT_NOAPP = False
if hasattr(_settings, 'APP_MANAGER_INTERCEPT_NOAPP'):
    INTERCEPT_NOAPP = _settings.APP_MANAGER_INTERCEPT_NOAPP
