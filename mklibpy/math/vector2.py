import math

from . import vector

__author__ = 'Michael'


class Vector2(vector.Vector):
    Length = 2
    AttrNames = {"x": 0, "y": 1}

    def angle(self):
        return math.atan2(self.y, self.x)


zero = Vector2.zero_int()
x_unit = Vector2.unit_int(0)
y_unit = Vector2.unit_int(1)

right = x_unit
left = -right
forward = y_unit
backward = -forward
screen_down = y_unit
screen_up = -screen_down

Zero = Vector2.zero_float()
XUnit = Vector2.unit_float(0)
YUnit = Vector2.unit_float(1)

Right = XUnit
Left = -Right
Forward = YUnit
Backward = -Forward
ScreenDown = YUnit
ScreenUp = -ScreenDown
