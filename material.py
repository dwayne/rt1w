from collections import namedtuple
import random

from ray import Ray
from vec3 import Vec3

def random_in_unit_radius_sphere():
    one = Vec3(1, 1, 1)

    while True:
        s = 2*Vec3(random.random(), random.random(), random.random()) - one
        if s.squared_length() < 1:
            return s

ScatterInfo = namedtuple('ScatterInfo', ['scattered', 'attenuation'])

class Material:
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, ray, hit_info):
        raise NotImplementedError

class Lambertian(Material):
    def scatter(self, ray, hit_info):
        target = hit_info.p + hit_info.normal + random_in_unit_radius_sphere()
        scattered = Ray(hit_info.p, target - hit_info.p)
        attenuation = self.albedo

        return ScatterInfo(scattered, attenuation)

def reflect(v, n):
    return v - 2*v.dot(n)*n

class Metal(Material):
    def __init__(self, albedo, fuzz=0):
        super().__init__(albedo)

        # fuzz is the fuzziness or perturbation parameter
        # it determines the fuzziness of the reflections
        self.fuzz = min(1, max(0, fuzz)) # ensures 0 <= self.fuzz <= 1

    def scatter(self, ray, hit_info):
        # Idea: Make ray.direction a computed property that returns the
        # unit direction vector when first accessed
        # maybe call it unit_direction and leave direction unchanged
        reflected = reflect(ray.direction.unit(), hit_info.normal)
        scattered = Ray(hit_info.p, reflected + self.fuzz*random_in_unit_radius_sphere())
        attenuation = self.albedo

        if scattered.direction.dot(hit_info.normal) > 0:
            return ScatterInfo(scattered, attenuation)

        return None
