import os

import tornado.web as _web

__author__ = 'Michael Kim'


class UrlBindingClashError(Exception):
    def __init__(self, url, method):
        self.__url = url
        self.__method = method

    def __str__(self):
        return "Url binding \"{}\" ({}) has already been defined".format(
            self.__url,
            "any" if self.__method is None else self.__method
        )


class HttpMethodError(Exception):
    def __init__(self, method):
        self.__method = method

    def __str__(self):
        return "Method \"{}\" not allowed".format(self.__method)


class ReturnValueError(Exception):
    def __init__(self, val, msg):
        self.__val = val
        self.__msg = msg

    def __str__(self):
        return self.__msg


class UrlBindings(object):
    def __init__(self):
        self.__bindings = {}

    def add(self, func, url, method=None):
        if method not in [None, "get", "post"]:
            raise HttpMethodError(method)
        if url in self.__bindings:
            methods = self.__bindings[url]
            if (method is None) or (None in methods) or (method in methods):
                raise UrlBindingClashError(url, method)
        else:
            methods = {}
            self.__bindings[url] = methods
        methods[method] = func

    @staticmethod
    def __gen_method(func):
        def __method(self: _web.RequestHandler):
            val = func(self)

            if val is None:
                return
            if isinstance(val, str):
                self.write(val)
                return
            if not isinstance(val, dict):
                raise ReturnValueError(val, "Return value is not `None`, `str` or `dict`")

            # header
            if "redirect" in val:
                self.redirect(val["redirect"])
                self.finish()
                return
            if "status" in val:
                status = val["status"]
                self.set_status(status)
            if "header" in val:
                header = val["header"]
                for key in header:
                    self.add_header(key, header[key])

            # body
            if "data" in val:
                self.write(val["data"])
                self.finish()
                return
            if "render" in val:
                render = val["render"]
                if "page" not in render:
                    raise ReturnValueError(val, "Key \"page\" not found in \"render\"")
                page = render["page"]
                if "args" in render:
                    args = render["args"]
                else:
                    args = {}
                self.render(page, **args)
                self.finish()
                return

        return __method

    def get_handlers(self):
        handlers = []
        for url in self.__bindings:
            methods = self.__bindings[url]
            get_method = None
            post_method = None
            if None in methods:
                get_method = post_method = methods[None]
            if "get" in methods:
                get_method = methods["get"]
            if "post" in methods:
                post_method = methods["post"]

            class __NewHandler(_web.RequestHandler):
                def get_template_path(self):
                    path = _web.RequestHandler.get_template_path(self)
                    if path is not None:
                        return path
                    return os.getcwd()

            if get_method is not None:
                __NewHandler.get = UrlBindings.__gen_method(get_method)
            if post_method is not None:
                __NewHandler.post = UrlBindings.__gen_method(post_method)

            handlers.append((url, __NewHandler))

        return handlers
