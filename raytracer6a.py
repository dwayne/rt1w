import math
import random
import sys

from camera import Camera
from objects import Hitable, HitableList, HitInfo, Sphere
from ray import Ray
from vec3 import Vec3

def random_in_unit_radius_sphere():
    one = Vec3(1, 1, 1)

    while True:
        s = 2*Vec3(random.random(), random.random(), random.random()) - one
        if s.squared_length() < 1:
            return s

def color(ray, world):
    hit_info = world.hit(ray, 0, sys.float_info.max)

    if hit_info:
        target = hit_info.p + hit_info.normal + random_in_unit_radius_sphere()

        # I think the 0.5 represents 50% reflection
        return 0.5 * color(Ray(hit_info.p, target - hit_info.p), world)

    unit_direction = ray.direction.unit()
    t = 0.5 * (unit_direction.y + 1)
    white = Vec3(1, 1, 1)
    blue = Vec3(0.5, 0.7, 1)

    return (1-t)*white + t*blue

width = 200
height = 100
samples = 100

print('P3\n%d %d\n255' % (width, height))


world = HitableList([
    Sphere(Vec3(0, 0, -1), 0.5),
    Sphere(Vec3(0, -100.5, -1), 100)
])

camera = Camera()

for y in range(height-1, -1, -1):
    for x in range(width):
        c = Vec3()
        for i in range(samples):
            u = (x + random.random()) / width
            v = (y + random.random()) / height

            r = camera.ray(u, v)
            c += color(r, world)

        c /= samples

        # gamma correction, using "gamma 2"
        c = Vec3(math.sqrt(c[0]), math.sqrt(c[1]), math.sqrt(c[2]))

        ir = int(255.99 * c[0])
        ig = int(255.99 * c[1])
        ib = int(255.99 * c[2])

        print('%d %d %d' % (ir, ig, ib))
