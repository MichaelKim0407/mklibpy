import math as _math

import mklibpy.error as _error
import mklibpy.util as _util
from . import collection as _collection

__author__ = 'Michael'


class Vector(_collection.StandardList):
    """
    The abstract vector class. Please use a subclass.
    All subclasses must have Length specified.
    """
    CONVERSION_ACCEPT_LIST = False
    CONVERSION_ACCEPT_TUPLE = True

    Length = None
    AttrNames = {}

    def __init__(self, *values, **kwargs):
        if self.__class__.Length is None:
            list.__init__(self, values)
        else:
            list.__init__(self)
            zero = kwargs["zero"] if "zero" in kwargs else None
            for i in range(self.__class__.Length):
                if i < len(values):
                    list.append(self, values[i])
                else:
                    list.append(self, zero)

    def __getattribute__(self, item):
        if item != "__class__" and item in self.__class__.AttrNames:
            return self[self.__class__.AttrNames[item]]
        else:
            return object.__getattribute__(self, item)

    # Formatting

    def __repr__(self):
        return self.__class__.__name__ + " " + _util.collection.format_list(self, start="(", end=")")

    def __str__(self):
        return _util.collection.format_list(self, start="", end="", sep=" ")

    def __format__(self, spec):
        return self.format(spec).__str__()

    # Conversion

    def convert(self, func):
        return self.__class__(*[func(x) for x in self])

    def int(self):
        return self.convert(int)

    def float(self):
        return self.convert(float)

    def format(self, spec):
        return self.convert(lambda x: format(x, spec))

    # Comparison

    def check_length(self, other):
        if not isinstance(other, Vector):
            raise TypeError(other)
        if list.__len__(self) != list.__len__(other):
            raise _error.VectorLengthError(self, other)

    def __eq__(self, other):
        self.check_length(other)
        for i in self.range():
            if self[i] != other[i]:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    # Dimensions

    def range(self):
        return range(len(self))

    def select(self, id_list, vec_type=None):
        if vec_type is None:
            vec_type = Vector
        return vec_type(*[self[i] for i in id_list])

    def reduce(self, n, vec_type=None):
        return self.select(range(n), vec_type)

    def slice(self, i, j, vec_type=None):
        return self.select(range(i, j), vec_type)

    def extend(self, n, vec_type=None, val=None):
        return vec_type(*(list(self) + [val] * (n - len(self))))

    # Calculation

    @classmethod
    def add_operator(cls, method_name):
        def method(self):
            return cls(*[getattr(x, method_name)() for x in self])

        setattr(cls, method_name, method)

    @classmethod
    def add_operator_bi(cls, method_name):
        def method(self, other):
            self.check_length(other)
            return cls(*[getattr(self[i], method_name)(other[i]) for i in self.range()])

        setattr(cls, method_name, method)

    def __neg__(self):
        return self.__class__(*[-x for x in self])

    def __add__(self, other):
        self.check_length(other)
        return self.__class__(*[self[i] + other[i] for i in self.range()])

    def __sub__(self, other):
        self.check_length(other)
        return self.__class__(*[self[i] - other[i] for i in self.range()])

    def __mul__(self, other):
        if isinstance(other, Vector):
            self.check_length(other)
            result = 0
            for i in self.range():
                result += self[i] * other[i]
            return result
        else:
            return self.__class__(*[x * other for x in self])

    def __rmul__(self, other):
        return self * other

    def squared(self):
        return self * self

    def length(self):
        return (self * self) ** 0.5

    # Constant

    @classmethod
    def identical(cls, value, length=None):
        if length is None:
            if cls.Length is None:
                raise ValueError(length)
            length = cls.Length
        return cls(*[value] * length)

    @classmethod
    def zero_int(cls, length=None):
        return cls.identical(0, length)

    @classmethod
    def zero_float(cls, length=None):
        return cls.identical(0.0, length)

    @classmethod
    def unit(cls, zero, value, i, length=None):
        if length is None:
            if cls.Length is None:
                raise ValueError(length)
            length = cls.Length
        return cls(*([zero] * i + [value] + [zero] * (length - i - 1)))

    @classmethod
    def unit_int(cls, i, length=None):
        return cls.unit(0, 1, i, length)

    @classmethod
    def unit_float(cls, i, length=None):
        return cls.unit(0.0, 1.0, i, length)


class Vector2(Vector):
    """
    A two-dimensional vector.
    """

    Length = 2
    AttrNames = {"x": 0, "y": 1}

    def angle(self):
        return _math.atan2(self.y, self.x)


Vector2.zero = Vector2.zero_int()
Vector2.x_unit = Vector2.unit_int(0)
Vector2.y_unit = Vector2.unit_int(1)

Vector2.right = Vector2.x_unit
Vector2.left = -Vector2.right
Vector2.forward = Vector2.y_unit
Vector2.backward = -Vector2.forward
Vector2.screen_down = Vector2.y_unit
Vector2.screen_up = -Vector2.screen_down

Vector2.Zero = Vector2.zero_float()
Vector2.XUnit = Vector2.unit_float(0)
Vector2.YUnit = Vector2.unit_float(1)

Vector2.Right = Vector2.XUnit
Vector2.Left = -Vector2.Right
Vector2.Forward = Vector2.YUnit
Vector2.Backward = -Vector2.Forward
Vector2.ScreenDown = Vector2.YUnit
Vector2.ScreenUp = -Vector2.ScreenDown


class Vector3(Vector):
    """
    A three-dimensional vector.
    """

    Length = 3
    AttrNames = {"x": 0, "y": 1, "z": 2}

    def cross(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def angle_from(self, other):
        return _math.degrees(_math.acos(self * other / (self.length() * other.length)))


Vector3.zero = Vector3.zero_int()
Vector3.x_unit = Vector3.unit_int(0)
Vector3.y_unit = Vector3.unit_int(1)
Vector3.z_unit = Vector3.unit_int(2)

Vector3.right = Vector3.x_unit
Vector3.left = -Vector3.right
Vector3.forward = Vector3.y_unit
Vector3.backward = -Vector3.forward
Vector3.up = Vector3.z_unit
Vector3.down = -Vector3.up

Vector3.Zero = Vector3.zero_float()
Vector3.XUnit = Vector3.unit_float(0)
Vector3.YUnit = Vector3.unit_float(1)
Vector3.ZUnit = Vector3.unit_float(2)

Vector3.Right = Vector3.XUnit
Vector3.Left = -Vector3.Right
Vector3.Forward = Vector3.YUnit
Vector3.Backward = -Vector3.Forward
Vector3.Up = Vector3.ZUnit
Vector3.Down = -Vector3.Up
