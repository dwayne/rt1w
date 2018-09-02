from collections import namedtuple
import math

HitInfo = namedtuple('HitInfo', ['t', 'p', 'normal'])

class Hitable:
    def hit(self, ray, t_min, t_max, hit_info):
        raise NotImplementedError

class Sphere(Hitable):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def hit(self, ray, t_min, t_max):
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(oc)
        c = oc.dot(oc) - self.radius*self.radius
        discriminant = b*b - 4*a*c

        if discriminant > 0:
            temp = (-b - math.sqrt(discriminant)) / (2*a)
            if t_min < temp < t_max:
                t = temp
                p = ray(t)
                normal = (p - self.center) / self.radius

                return HitInfo(t, p, normal)

            temp = (-b + math.sqrt(discriminant)) / (2*a)
            if t_min < temp < t_max:
                t = temp
                p = ray(t)
                normal = (p - self.center) / self.radius

                return HitInfo(t, p, normal)

        return None

class HitableList(list, Hitable):
    def hit(self, ray, t_min, t_max):
        hit_anything = False
        closest_so_far = t_max

        for obj in self:
            hit_info = obj.hit(ray, t_min, closest_so_far)
            if hit_info:
                hit_anything = True
                closest_so_far = hit_info.t
                result_info = hit_info

        if hit_anything:
            return result_info

        return None
