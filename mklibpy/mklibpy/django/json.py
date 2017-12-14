import django.http as _http

__author__ = 'Michael'


class JsonErrorResponse(Exception):
    """
    An error response intended to be transformed into a JsonResponse by JsonResponseWrapper.

    You may subclass this class to create Errors with specific error codes or messages,
    e.g.

    class MyError(JsonErrorResponse):
        CODE = 1
        MSG = "my error"
    """
    CODE = None
    MSG = None

    def __init__(self, code=None, msg=None, data=None):
        self.__code = code or self.CODE
        if not self.__code:
            raise ValueError("error code must be non-zero")

        self.__msg = msg or self.MSG
        self.__data = data

    def get_object(self):
        return {
            'code': self.__code,
            'msg': self.__msg,
            'data': self.__data
        }

    def get_response(self):
        return _http.JsonResponse(self.get_object())


class JsonResponseWrapper(object):
    """
    A middleware that, if the value returned by a view is not HttpResponse,
    wrap it into a JsonResponse in the following form:

    JsonResponse({
        'code': 0,
        'data': return value
    })

    Also, if a JsonErrorResponse is raised in the view,
    this middleware will turn it into a JsonResponse with specified
    error code, message and data.

    If used with other middlewares such as PageWrapper or ModelWrapper,
    this middleware needs to be the outermost one.
    """

    def __init__(self, get_response):
        self.__get_response = get_response

    def __call__(self, request):
        response = self.__get_response(request)

        if isinstance(response, _http.HttpResponse):
            return response
        else:
            return _http.JsonResponse({
                'code': 0,
                'data': response
            })

    def process_exception(self, request, e):
        if isinstance(e, JsonErrorResponse):
            return e.get_response()
        else:
            return None
