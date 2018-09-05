import math
import random

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

class FOVCamera:
    def __init__(self, vfov, aspect):
        # vfov is top to bottom in degrees
        theta = math.radians(vfov)
        half_height = math.tan(theta / 2)
        half_width = aspect * half_height

        self._lower_left_corner = Vec3(-half_width, -half_height, -1)
        self._horizontal = Vec3(x=2 * half_width)
        self._vertical = Vec3(y=2 * half_height)
        self._origin = Vec3()

    def ray(self, u, v):
        return Ray(self._origin, self._lower_left_corner + u*self._horizontal + v*self._vertical)

class PositionalCamera:
    def __init__(self, lookfrom, lookat, vup, vfov, aspect):
        theta = math.radians(vfov)
        half_height = math.tan(theta / 2)
        half_width = aspect * half_height

        w = (lookfrom - lookat).unit()
        u = vup.cross(w).unit()
        v = w.cross(u)

        self._lower_left_corner = Vec3(-half_width, -half_height, -1)
        self._lower_left_corner = lookfrom - half_width*u - half_height*v - w
        self._horizontal = 2 * half_width * u
        self._vertical = 2 * half_height * v
        self._origin = lookfrom

    def ray(self, u, v):
        return Ray(self._origin, self._lower_left_corner + u*self._horizontal + v*self._vertical - self._origin)

def random_in_unit_disc():
    while True:
        p = 2 * Vec3(random.random(), random.random()) - Vec3(1, 1)
        if p.dot(p) < 1:
            return p

class DOFCamera:
    def __init__(self, lookfrom, lookat, vup, vfov, aspect, aperture, focus_dist):
        theta = math.radians(vfov)
        half_height = math.tan(theta / 2)
        half_width = aspect * half_height

        w = (lookfrom - lookat).unit()
        self._u = u = vup.cross(w).unit()
        self._v = v = w.cross(u)

        self._lens_radius = aperture / 2
        self._lower_left_corner = lookfrom - half_width*focus_dist*u - half_height*focus_dist*v - focus_dist*w
        self._horizontal = 2 * half_width * focus_dist * u
        self._vertical = 2 * half_height * focus_dist * v
        self._origin = lookfrom

    def ray(self, u, v):
        rd = self._lens_radius * random_in_unit_disc()
        offset = rd.x*self._u + rd.y*self._v
        return Ray(self._origin + offset, self._lower_left_corner + u*self._horizontal + v*self._vertical - self._origin - offset)
