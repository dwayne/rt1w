import math
import random
import sys

from camera import FOVCamera
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
    Sphere(Vec3(-R, 0, -1), R, Lambertian(Vec3(0, 0, 1))),
    Sphere(Vec3(R, 0, -1), R, Lambertian(Vec3(1, 0, 0)))
])

camera = FOVCamera(90, width / height)

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
