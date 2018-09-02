import math
import numbers

class Vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    # Let k be a scalar and u, v be vectors

    # u[0] == x
    # u[1] == y
    # u[2] == z
    def __getitem__(self, i):
        if i == 0:
            return self.x

        if i == 1:
            return self.y

        if i == 2:
            return self.z

        if isinstance(i, numbers.Integral):
            raise IndexError('vector index out of range')
        else:
            raise TypeError('vector indices must be integers, not %s' % type(i).__name__)

    # +u
    def __pos__(self):
        return self

    # -u
    def __neg__(self):
        return __class__(-self.x, -self.y, -self.z)

    # u + v
    def __add__(self, other):
        return __class__(self.x + other.x, self.y + other.y, self.z + other.z)

    # u - v
    def __sub__(self, other):
        return __class__(self.x - other.x, self.y - other.y, self.z - other.z)

    # u * v
    def __mul__(self, other):
        return __class__(self.x * other.x, self.y * other.y, self.z * other.z)

    # u / k or u / v
    def __truediv__(self, other):
        if isinstance(other, numbers.Real):
            return __class__(self.x / other, self.y / other, self.z / other)

        return __class__(self.x / other.x, self.y / other.y, self.z / other.z)

    # k * u
    def __rmul__(self, other):
        return __class__(other * self.x, other * self.y, other * self.z)

    # length of u
    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    # N.B. Can't use __len__ since we need to return a floating-point value

    # squared length of u
    def squared_length(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    # dot product
    # ref: https://en.wikipedia.org/wiki/Dot_product
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    # cross product
    # ref: https://en.wikipedia.org/wiki/Cross_product
    def cross(self, other):
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x

        return __class__(x, y, z)

    # unit vector
    def unit(self):
        return self / self.length()

    def __repr__(self):
        return '%s(%.3f, %.3f, %.3f)' % (__class__.__name__, self.x, self.y, self.z)
