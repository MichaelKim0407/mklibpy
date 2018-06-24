import json as _json
import tornado.ioloop as _ioloop
import tornado.web as _web

from . import binding
from .. import code as _code

__author__ = 'Michael Kim'

__version__ = "0.1.3"

__url_bindings = binding.UrlBindings()


def bind_url(url, method=None):
    def __decor(func):
        __url_bindings.add(func, url, method)
        return func

    return __decor


def params(pass_body=None, lists=(), **kwargs):
    if pass_body is True:
        pass_body = 'body'

    def __decor(func):
        args = _code.func.FuncArgs(func)

        def __new_func(self: _web.RequestHandler):
            params = {}
            for arg in args:
                if arg == pass_body:
                    value = self.request.body
                elif arg in lists:
                    value = self.request.get_arguments(arg)
                    if arg in kwargs:
                        value = [kwargs[arg](v) for v in value]
                else:
                    if arg in args.defaults:
                        value = self.request.get_argument(arg, default=args.defaults[arg])
                    else:
                        value = self.request.get_argument(arg)
                    if arg in kwargs:
                        value = kwargs[arg](value)
                params[arg] = value
            return func(**params)

        return __new_func

    return __decor


def json(data=None):
    return {
        "header": {
            "Content-Type": "application/json;charset=UTF-8"
        },
        "data": "{}" if data is None else _json.dumps(data)
    }


def start(port, **kwargs):
    app = _web.Application(
        __url_bindings.get_handlers(),
        **kwargs
    )
    app.listen(port)
    _ioloop.IOLoop.instance().start()
