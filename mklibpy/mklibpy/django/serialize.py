import django.db.models as _models
import django.http as _http

__author__ = 'Michael'

__SERIALIZE_METHOD_NAME = 'serialize'
__SERIALIZE_EXTEND_METHOD_NAME = 'serialize_extend'


class SerializeProperty(object):
    """
    A property that is intended to be serialized.

    Usage: see `serialize_property`
    """

    def __init__(self, func, name):
        self.__func = func
        self.name = name

    def __call__(self, *args, **kwargs):
        return self.__func(*args, **kwargs)


def serialize_property(name=None):
    """
    A decorator that marks a class method as intended for serialization.

    :param name: The key for serialization.
                 If left None, the name of the method will be used,
                 with the exception that, if the name starts with "get_",
                 the part after that will be used.

    e.g.

    class MyModel(models.Model):
        some fields

        @serialize_property()
        def get_x():
            return stuff

    See also: serialize
    """

    def __decor(func):
        if name is not None:
            property_name = name
        elif func.__name__.startswith("get_"):
            property_name = func.__name__[4:]
        else:
            property_name = func.__name__

        p = SerializeProperty(func, property_name)

        return p

    return __decor


def serialize(obj):
    """
    Serialize a Model instance into a dict.

    The instance will be serialized with the following strategy:

    - If a method named `serialize` exists, use the result for that method.
      The method MUST return a dict.
      All the following steps are ignored.

    - Find all the fields defined in the class, and use their names and values.
    - Find all SerializeProperty's defined in the class, and add their names and values.
    - If a method named `serialize_extend` exists, add the result for that method.
      The method MUST return a dict.

    :param obj: The model instance.
    """

    if hasattr(obj, __SERIALIZE_METHOD_NAME):
        return getattr(obj, __SERIALIZE_METHOD_NAME)()

    result = {field.name: field.value_from_object(obj)
              for field in obj._meta.get_fields()
              if isinstance(field, _models.Field)}

    for attr in obj.__class__.__dict__.values():
        if isinstance(attr, SerializeProperty):
            result[attr.name] = attr(obj)

    if not hasattr(obj, __SERIALIZE_EXTEND_METHOD_NAME):
        return result

    result.update(getattr(obj, __SERIALIZE_EXTEND_METHOD_NAME)())
    return result


def is_query_set(obj):
    return isinstance(obj, _models.Manager) \
           or isinstance(obj, _models.QuerySet)


def is_query_object(obj):
    return isinstance(obj, _models.Model)


def is_query_result(obj):
    return is_query_set(obj) or is_query_object(obj)


def serialize_all(obj):
    """
    Recursively iterate through all lists/dicts.
    """
    if is_query_set(obj):
        return [serialize(o) for o in obj.all()]
    elif is_query_object(obj):
        return serialize(obj)

    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = serialize_all(obj[i])
    elif isinstance(obj, dict):
        for key in obj:
            obj[key] = serialize_all(obj[key])

    return obj


class ModelWrapper(object):
    """
    A middleware that, if the value returned by the view is not an HttpResponse,
    find all Model instances or query results contained in the return value,
    and serialize those instances/results.

    To specify how a Model instance should be serialized,
    see serialize.

    Should be used with JsonResponseWrapper on the outside,
    unless there is another middleware that turns raw values into HttpResponse.
    If used with PageWrapper, this middleware needs to be on the outside.
    """

    def __init__(self, get_response):
        self.__get_response = get_response

    def __call__(self, request):
        response = self.__get_response(request)

        if isinstance(response, _http.HttpResponse):
            return response

        return serialize_all(response)
