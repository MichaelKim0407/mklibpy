import math

from . import vector

__author__ = 'Michael'


class Vector3(vector.Vector):
    Length = 3
    AttrNames = {"x": 0, "y": 1, "z": 2}

    def cross(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def angle_from(self, other):
        return math.degrees(math.acos(self * other / (self.length() * other.length)))


zero = Vector3.zero_int()
x_unit = Vector3.unit_int(0)
y_unit = Vector3.unit_int(1)
z_unit = Vector3.unit_int(2)

right = x_unit
left = -right
forward = y_unit
backward = -forward
up = z_unit
down = -up

Zero = Vector3.zero_float()
XUnit = Vector3.unit_float(0)
YUnit = Vector3.unit_float(1)
ZUnit = Vector3.unit_float(2)

Right = XUnit
Left = -Right
Forward = YUnit
Backward = -Forward
Up = ZUnit
Down = -Up
