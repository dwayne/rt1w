from ray import Ray
from vec3 import Vec3

def hit_sphere(center, radius, ray):
    oc = ray.origin - center
    a = ray.direction.dot(ray.direction)
    b = 2 * ray.direction.dot(oc)
    c = oc.dot(oc) - radius*radius
    discriminant = b*b - 4*a*c

    return discriminant > 0 # why not >= 0?

def color(ray):
    if hit_sphere(Vec3(0, 0, -1), 0.5, ray):
        return Vec3(1)

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
