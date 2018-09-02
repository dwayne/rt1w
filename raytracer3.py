import math

from ray import Ray
from vec3 import Vec3

def hit_sphere(center, radius, ray):
    oc = ray.origin - center
    a = ray.direction.dot(ray.direction)
    b = 2 * ray.direction.dot(oc)
    c = oc.dot(oc) - radius*radius
    discriminant = b*b - 4*a*c

    if discriminant < 0:
        return -1 # missed

    return (-b - math.sqrt(discriminant)) / (2*a)

def color(ray):
    center = Vec3(0, 0, -1)
    t = hit_sphere(center, 0.5, ray)
    if t > 0:
        # compute the normal at the hit point
        n = (ray(t) - center).unit()

        # since n is a unit vector, -1 <= n.x, n.y, n.z <= 1
        # => n + (1, 1, 1) gives 0 <= n.x, n.y, n.z <= 2
        # => 0.5 * n gives 0 <= n.x, n.y, n.z <= 1
        return 0.5 * (n + Vec3(1, 1, 1))

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

for y in range(height-1, -1, -1):
    for x in range(width):
        u = x / width
        v = y / height

        r = Ray(origin, lower_left_corner + u*horizontal + v*vertical)
        c = color(r)

        ir = int(255.99 * c[0])
        ig = int(255.99 * c[1])
        ib = int(255.99 * c[2])

        print('%d %d %d' % (ir, ig, ib))
