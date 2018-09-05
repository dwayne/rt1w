import math
import random
import sys

from camera import DOFCamera
from material import Dielectric, Lambertian, Metal
from objects import Hitable, HitableList, HitInfo, Sphere
from ray import Ray
from vec3 import Vec3

def random_scene():
    scene = HitableList()
    scene.append(Sphere(Vec3(0, -1000, 0), 1000, Lambertian(Vec3(0.5, 0.5, 0.5))))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random.random()
            center = Vec3(a+0.9*random.random(), 0.2, b+0.9*random.random())
            if (center - Vec3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    # diffuse
                    scene.append(Sphere(center, 0.2, Lambertian(Vec3(random.random()*random.random(), random.random()*random.random(), random.random()*random.random()))))
                elif choose_mat < 0.95:
                    # metal
                    scene.append(Sphere(center, 0.2, Metal(Vec3(0.5*(1 + random.random()), 0.5*(1 + random.random()), 0.5*(1 + random.random())), 0.5*random.random())))
                else:
                    # glass
                    scene.append(Sphere(center, 0.2, Dielectric(1.5)))

    scene.append(Sphere(Vec3(0, 1, 0), 1, Dielectric(1.5)))
    scene.append(Sphere(Vec3(-4, 1, 0), 1, Lambertian(Vec3(0.4, 0.2, 0.1))))
    scene.append(Sphere(Vec3(4, 1, 0), 1, Metal(Vec3(0.7, 0.6, 0.5))))

    return scene

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

world = random_scene()

lookfrom = Vec3(3, 3, 2)
lookat = Vec3(0, 0, -1)
dist_to_focus = (lookfrom - lookat).length()
aperture = 2
camera = DOFCamera(lookfrom, lookat, Vec3(0, 1, 0), 20, width / height, aperture, dist_to_focus)

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
