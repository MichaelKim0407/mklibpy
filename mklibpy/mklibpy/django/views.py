import django.http as _http
from django.shortcuts import render as _render

from .. import code as _code

__author__ = 'Michael'


class RequiredParameterNotFound(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Required parameter '{}' not found".format(self.name)


def __get_params_def(func, types, start=0):
    argcount = func.__code__.co_argcount
    func_args = func.__code__.co_varnames[:argcount]
    defaults = len(func.__defaults__) if func.__defaults__ is not None else 0

    def __yield():
        for i in range(start, argcount):
            name = func_args[i]
            if name in types:
                type = types[name]
            else:
                type = str
            required = i + defaults < argcount
            yield name, type, required

    return list(__yield())


def __get_parameters(params_def, provider):
    parameters = {}

    for name, type, required in params_def:
        if name not in provider:
            if required:
                raise RequiredParameterNotFound(name)
            else:
                continue
        val = type(provider[name])
        parameters[name] = val

    return parameters


def view(pass_request=None, **kwargs):
    """
    Decorate a function with named parameters, rewriting it as a view.

    :param pass_request:
        If None, do not pass `request`;
        If True, pass `request` into 'request' argument;
        If str, the named argument to pass `request` into.
    :param kwargs:
        Specify types for parameters.
        Unspecified parameters will have the default type `str`.
    :return: The view.

    e.g.

    @view(x=int)
    def f(name, x):
        name is the value of request param `name`
        x is the int value of request param `x`
    """
    if pass_request is True:
        pass_request = 'request'

    def __decor(func):
        args = _code.func.FuncArgs(func)

        def __view(request):
            d = getattr(request, request.method).copy()
            if pass_request:
                d[pass_request] = request

            params = args.push(**d)
            for param in kwargs:
                if param not in params:
                    continue
                params[param] = kwargs[param](params[param])

            return func(**params)

        return __view

    return __decor


def render():
    """
    Decorates a view-like function, passing its return values to `django.shortcuts.render`.

    - If the return value is a str, call render(request, result).
    - If the return value is a tuple, call render(request, *result).
    - If the return value is a dict, call render(request, **result).

    e.g.

    @render()
    @view()
    def index():
        return 'index.html'
    """

    def __decor(view_func):

        def __view(request):
            result = view_func(request)

            if isinstance(result, _http.HttpResponse):
                return result

            if isinstance(result, str):
                return _render(request, result)
            elif isinstance(result, tuple):
                return _render(request, *result)
            elif isinstance(result, dict):
                return _render(request, **result)
            else:
                raise TypeError("return type with @render must be str, tuple or dict")

        return __view

    return __decor


def combine(**kwargs):
    """
    Decorates a view-like function and creates a new view that,
    based on the request method (GET/POST),
    process the request with another view.

    If the view body is not empty, it will be called first.
    If the function returns a value that is not None,
    the value is immediately returned and no method-based view will be called.

    e.g.

    @render()
    def __get_form():
        return 'form.html'

    @view()
    def __post_form():
        do stuff here

    @combine(GET=__get_form, POST=__post_form)
    @view(id=int)
    def form(id):
        if id not in xxx:
            return HttpResponseBadRequest()
    """

    def __decor(func):
        def __view(request):
            init = func(request)
            if init is not None:
                return init

            if request.method not in kwargs:
                return _http.HttpResponseNotAllowed(kwargs.keys())

            return kwargs[request.method](request)

        return __view

    return __decor


def method(*args):
    """
    Decorates a view, limit the request method.

    e.g.

    @method('GET')
    @render()
    @view()
    def index():
        return 'index.html'
    """

    def __decor(view_func):
        def __view(request):
            if request.method not in args:
                return _http.HttpResponseNotAllowed(args)
            return view_func(request)

        return __view

    return __decor
