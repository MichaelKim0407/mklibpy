import json as _json

import tornado.ioloop as _ioloop
import tornado.web as _web

from . import binding
from . import param

__author__ = 'Michael Kim'

__version__ = "0.1.3"

__url_bindings = binding.UrlBindings()
__params = {}


def bind_url(url, method=None):
    def __decor(func):
        __url_bindings.add(func, url, method)
        __params[func] = param.Params(func)
        return func

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
        __url_bindings.get_handlers(__params),
        **kwargs
    )
    app.listen(port)
    _ioloop.IOLoop.instance().start()
