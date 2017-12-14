from django.http import Http404

import logging
from . import settings, models

__author__ = 'Michael'

logger = logging.getLogger('mklibpy.django.app_manager.intercept')


class AppNameInterceptor(object):
    def __init__(self, get_response):
        self.__get_response = get_response

    def __call__(self, request):
        response = self.__get_response(request)

        app_name = request.resolver_match.app_name
        if not app_name:
            if settings.INTERCEPT_NOAPP:
                logger.info("Intercepted no_app")
                raise Http404
            return response

        try:
            app = models.App.objects.get(name=app_name)
        except models.App.DoesNotExist:
            # Not registered in the database
            if settings.INTERCEPT_UNREGISTERED:
                logger.info("Intercepted unregistered app '{}'".format(app_name))
                raise Http404
            return response
        if not app.active:
            logger.info("Intercepted inactive app '{}'".format(app_name))
            raise Http404

        return response
