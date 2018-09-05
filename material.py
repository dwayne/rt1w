from collections import namedtuple
import math
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
    def scatter(self, ray, hit_info):
        raise NotImplementedError

class Lambertian(Material):
    def __init__(self, albedo):
        super().__init__()
        self.albedo = albedo

    def scatter(self, ray, hit_info):
        target = hit_info.p + hit_info.normal + random_in_unit_radius_sphere()
        scattered = Ray(hit_info.p, target - hit_info.p)
        attenuation = self.albedo

        return ScatterInfo(scattered, attenuation)

def reflect(v, n):
    return v - 2*v.dot(n)*n

class Metal(Material):
    def __init__(self, albedo, fuzz=0):
        super().__init__()
        self.albedo = albedo

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

def refract(v, n, ni_over_nt):
    uv = v.unit()
    dt = uv.dot(n)
    discriminant = 1 - ni_over_nt*ni_over_nt*(1 - dt*dt)
    if discriminant > 0:
        return ni_over_nt*(uv - dt*n) - math.sqrt(discriminant)*n

    return None

def schlick(cosine, refractive_index):
    r0 = (1 - refractive_index) / (1 + refractive_index)
    r0 *= r0
    return r0 + (1 - r0) * pow(1 - cosine, 5)

class Dielectric(Material):
    def __init__(self, refractive_index):
        super().__init__()
        self.refractive_index = refractive_index

    def scatter(self, ray, hit_info):
        reflected = reflect(ray.direction, hit_info.normal)
        attenuation = Vec3(1, 1, 1)

        if ray.direction.dot(hit_info.normal) > 0:
            outward_normal = -hit_info.normal
            ni_over_nt = self.refractive_index
            cosine = self.refractive_index * ray.direction.dot(hit_info.normal) / ray.direction.length()
        else:
            outward_normal = hit_info.normal
            ni_over_nt = 1 / self.refractive_index
            cosine = -ray.direction.dot(hit_info.normal) / ray.direction.length()

        refracted = refract(ray.direction, outward_normal, ni_over_nt)
        if refracted:
            reflect_prob = schlick(cosine, self.refractive_index)
        else:
            reflect_prob = 1

        if random.random() < reflect_prob:
            return ScatterInfo(Ray(hit_info.p, reflected), attenuation)

        return ScatterInfo(Ray(hit_info.p, refracted), attenuation)
