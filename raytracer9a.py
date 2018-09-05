import math
import random
import sys

from camera import PositionalCamera
from material import Dielectric, Lambertian, Metal
from objects import Hitable, HitableList, HitInfo, Sphere
from ray import Ray
from vec3 import Vec3

def color(ray, world, depth):
    hit_info = world.hit(ray, 0.001, sys.float_info.max)

    if hit_info:
        zero = Vec3()

        if depth < 50:
            scatter_info = hit_info.material.scatter(ray, hit_info)
            if scatter_info:
                return scatter_info.attenuation * color(scatter_info.scattered, world, depth+1)
            else:
                return zero
        else:
            return zero

    unit_direction = ray.direction.unit()
    t = 0.5 * (unit_direction.y + 1)
    white = Vec3(1, 1, 1)
    blue = Vec3(0.5, 0.7, 1)

    return (1-t)*white + t*blue

width = 200
height = 100
samples = 100

print('P3\n%d %d\n255' % (width, height))

R = math.cos(math.pi / 4)

world = HitableList([
    Sphere(Vec3(0, 0, -1), 0.5, Lambertian(Vec3(0.1, 0.2, 0.5))),
    Sphere(Vec3(0, -100.5, -1), 100, Lambertian(Vec3(0.8, 0.8, 0))),
    Sphere(Vec3(1, 0, -1), 0.5, Metal(Vec3(0.8, 0.6, 0.2))),
    Sphere(Vec3(-1, 0, -1), 0.5, Dielectric(1.5)),
    Sphere(Vec3(-1, 0, -1), -0.45, Dielectric(1.5))
])

camera = PositionalCamera(Vec3(-2, 2, 1), Vec3(0, 0, -1), Vec3(0, 1, 0), 90, width / height)

for y in range(height-1, -1, -1):
    for x in range(width):
        c = Vec3()
        for i in range(samples):
            u = (x + random.random()) / width
            v = (y + random.random()) / height

            r = camera.ray(u, v)
            c += color(r, world, 0)

        c /= samples

        # gamma correction, using "gamma 2"
        c = Vec3(math.sqrt(c[0]), math.sqrt(c[1]), math.sqrt(c[2]))

        ir = int(255.99 * c[0])
        ig = int(255.99 * c[1])
        ib = int(255.99 * c[2])

        print('%d %d %d' % (ir, ig, ib))
