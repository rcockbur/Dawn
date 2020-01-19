from math import sqrt, atan, pi, degrees, atan2
from random import getrandbits

class Point:
    def __init__(self, x = 10, y = 10, point = None):
        if isinstance(point, Point):
            self.x = point.x
            self.y = point.y
        elif (isinstance(x, int) and isinstance(y, int)) or (isinstance(x, float) and isinstance(y, float)):
            self.x = x
            self.y = y
        else:
            raise ValueError("Invalid parameters x",type(x)," and y",type(y))

    def __eq__(self, obj):
        return type(obj) == Point and obj.x == self.x and obj.y == self.y

    def __add__(self, vector):
        if isinstance(vector, Vector):
            x = self.x + vector.x
            y = self.y + vector.y
            return Point(x, y)
        else:
            raise ValueError("Vector is required")

    def __radd__(self, vector):
        return self._add__(vector)


    def __sub__(self, point):
        if isinstance(point, Point):
            x = self.x - point.x
            y = self.y - point.y
            return Vector(x, y)
        else:
            raise ValueError("Point is required")

    def copy(self):
        return Point(x=self.x, y=self.y)

    def str(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, obj):
        return type(obj) == Vector and obj.x == self.x and obj.y == self.y

    def __add__(self, vector):
        if isinstance(vector, Vector):
            x = self.x + vector.x
            y = self.y + vector.y
            return Vector(x, y)
        else:
            raise ValueError("Vector is required")

    def __radd__(self, vector):
        return self._add__(vector)


    def __sub__(self, vector):
        if isinstance(vector, Vector):
            x = self.x - vector.x
            y = self.y - vector.y
            return Vector(x, y)
        else:
            raise ValueError("Vector is required")

    def flip(self):
        self.x = -self.x
        self.y = -self.y

    def size(self):
        if self.x != 0 or self.y != 0:
            return sqrt(self.x ** 2 + self.y ** 2)
        else:
            return 0

    def print(self):
        print("X:",self.x," Y:",self.y)

    def size_squared(self):
        return self.x ** 2 + self.y ** 2

    def to_direction_number(self):
        if self.x == 0 and self.y == 0:
            raise RuntimeError("Cannon normalize a zero vector")

        if self.x == 0:
            if self.y > 0:
                return 4
            else:
                return 0
        else:
            angle = (degrees(atan2(self.x, -self.y)))
            if angle < 0: angle += 360
            # print(round(angle / 45.0) % 8)
            return(round(angle / 45.0) % 8)

