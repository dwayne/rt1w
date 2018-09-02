class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def __call__(self, t):
        return self.origin + t * self.direction
