from ray import Ray
from vec3 import Vec3

class Camera:
    def __init__(self):
        self._lower_left_corner = Vec3(-2, -1, -1)
        self._horizontal = Vec3(x=4)
        self._vertical = Vec3(y=2)
        self._origin = Vec3()

    def ray(self, u, v):
        # 0 <= u, v <= 1
        return Ray(self._origin, self._lower_left_corner + u*self._horizontal + v*self._vertical)
