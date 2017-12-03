__author__ = 'Michael'


def __filters(filters, name, item):
    if not filters:
        return True
    for f in filters:
        if not f(name, item):
            return False
    return True


def get_self_members(cls, *filters):
    result = {}
    for name in cls.__dict__:
        item = cls.__dict__[name]
        if not __filters(filters, name, item):
            continue
        result[name] = item
    return result


def get_all_members(cls, *filters):
    result = get_self_members(cls, *filters)

    if cls.__base__ is None:  # object
        return result

    for name in get_all_members(cls.__base__):
        if name in result:
            continue
        item = getattr(cls, name)
        if not __filters(filters, name, item):
            continue
        result[name] = item

    return result


def filter_name(name_filter):
    def __filter(name, item):
        return name_filter(name)

    return __filter


def filter_item(item_filter):
    def __filter(name, item):
        return item_filter(item)

    return __filter
