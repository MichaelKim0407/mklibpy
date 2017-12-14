import django.db.models as _models
import django.utils.timezone as _timezone

from . import constants as _constants

__author__ = 'Michael'


class TinyIntegerField(_models.SmallIntegerField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == _constants.DB_BACKEND_MYSQL:
            return "TINYINT"
        else:
            return super().db_type(connection)


class FixedCharField(_models.CharField):
    def __init__(self, max_length, *args, **kwargs):
        self.__max_length = max_length
        super().__init__(max_length=max_length, *args, **kwargs)

    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == _constants.DB_BACKEND_MYSQL:
            return "CHAR({})".format(self.__max_length)
        else:
            return super().db_type(connection)


class _ManagedDateTimeField(_models.DateTimeField):
    def __init__(self, *args, **kwargs):
        kwargs['auto_now'] = False
        kwargs['auto_now_add'] = False
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if 'auto_now' in kwargs:
            del kwargs['auto_now']
        if 'auto_now_add' in kwargs:
            del kwargs['auto_now_add']
        return name, path, args, kwargs

    def _set_now(self, model_instance):
        value = _timezone.now()
        setattr(model_instance, self.attname, value)
        return value


class CreateTimeField(_ManagedDateTimeField):
    """
    A field representing the creation time.

    This field differs from a `DateTimeField(auto_now_add=True)` in the way that:
    - At the time of creation, it can be overridden;
      if blank, the current time will be used.
    """

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if not add:
            return value
        if value is not None:
            return value
        return self._set_now(model_instance)


class ModifyTimeField(_ManagedDateTimeField):
    """
    A field representing the modification time.

    This field differs from a `DateTimeField(auto_now=True)` in the way that:
    - At the time of creation, it can be overridden;
      if blank, the value will be null.
    - If `delete_flag` is not None,
      a field with corresponding named exists,
      and evaluates as True,
      the value will no longer be updated.
    """

    def __init__(self, delete_flag=None, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        self.__delete_flag = delete_flag
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if 'null' in kwargs:
            del kwargs['null']
        if 'blank' in kwargs:
            del kwargs['blank']
        kwargs['delete_flag'] = self.__delete_flag
        return name, path, args, kwargs

    def is_deleted(self, model_instance):
        if self.__delete_flag is None:
            return False
        if not hasattr(model_instance, self.__delete_flag):
            return False
        return getattr(model_instance, self.__delete_flag)

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if add:
            return value
        if self.is_deleted(model_instance):
            return value
        return self._set_now(model_instance)


class DeleteTimeField(_ManagedDateTimeField):
    """
    A field representing the deletion time.

    This field behaves as follows:
    - The field with a name of specified `delete_flag` must exist.
    - If the corresponding field evaluates as False,
      the value will always be None.
    - If the corresponding field evaluates as True,
        - At the time of creation, it can be overridden;
          if blank, the current time will be used.
        - The current time will be used if the field is None,
          i.e. it only updates for the first time.
    """

    def __init__(self, delete_flag, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        self.__delete_flag = delete_flag
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if 'null' in kwargs:
            del kwargs['null']
        if 'blank' in kwargs:
            del kwargs['blank']
        kwargs['delete_flag'] = self.__delete_flag
        return name, path, args, kwargs

    def is_deleted(self, model_instance):
        return getattr(model_instance, self.__delete_flag)

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if not self.is_deleted(model_instance):
            return None
        if value is not None:
            # If already deleted
            return value
        return self._set_now(model_instance)
