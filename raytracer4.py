import math
import sys

from objects import Hitable, HitableList, HitInfo, Sphere
from ray import Ray
from vec3 import Vec3

def color(ray, world):
    hit_info = world.hit(ray, 0, sys.float_info.max)

    if hit_info:
        return 0.5 * (hit_info.normal + Vec3(1, 1, 1))

    unit_direction = ray.direction.unit()
    t = 0.5 * (unit_direction.y + 1)
    white = Vec3(1, 1, 1)
    blue = Vec3(0.5, 0.7, 1)

    return (1-t)*white + t*blue

width = 200
height = 100

print('P3\n%d %d\n255' % (width, height))

lower_left_corner = Vec3(-2, -1, -1)
horizontal = Vec3(x=4)
vertical = Vec3(y=2)
origin = Vec3()
world = HitableList([
    Sphere(Vec3(0, 0, -1), 0.5),
    Sphere(Vec3(0, -100.5, -1), 100)
])

for y in range(height-1, -1, -1):
    for x in range(width):
        u = x / width
        v = y / height

        r = Ray(origin, lower_left_corner + u*horizontal + v*vertical)
        c = color(r, world)

        ir = int(255.99 * c[0])
        ig = int(255.99 * c[1])
        ib = int(255.99 * c[2])

        print('%d %d %d' % (ir, ig, ib))
