from ray import Ray
from vec3 import Vec3

def color(ray):
    unit_direction = ray.direction.unit()

    # -1 <= unit_direction.y <= 1
    # => 0 <= unit_direction.y + 1 <= 2
    # => 0 <= 0.5 * (unit_direction.y + 1) <= 1
    t = 0.5 * (unit_direction.y + 1)

    # when t = 0, we want white
    white = Vec3(1, 1, 1)

    # when t = 1, we want blue
    blue = Vec3(0.5, 0.7, 1)

    # in between, we want a blend
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
