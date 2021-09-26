import pygame as pg

from src.common.config import TOLERANCE


class BaseShape:
    def __init__(self, relative_pos: pg.math.Vector2 = pg.math.Vector2(0, 0)):
        self.relative_pos = relative_pos
        self.body = None

    def get_absolute_pos(self):
        return self.relative_pos + self.body.get_position()

    def collide_reflect_velocity(self, shape, velocity):
        pass

    def collide_reflect_position(self, shape):
        pass

    def collide_reflect_force(self, shape, force):
        return self.collide_reflect_velocity(shape, force)

    def collide_with(self, shape, velocity):
        pass


class PlaneShape(BaseShape):
    def __init__(self, normal: pg.math.Vector2, relative_pos: pg.math.Vector2 = pg.math.Vector2(0, 0)):
        super().__init__(relative_pos)
        self.normal = normal

    def collide_width(self, shape, velocity):
        pass


class CircleShape(BaseShape):
    def __init__(self, radius, relative_pos: pg.math.Vector2 = pg.math.Vector2(0, 0)):
        super().__init__(relative_pos)
        self.radius = radius

    def collide_reflect_velocity(self, shape, velocity):
        if isinstance(shape, CircleShape):
            v = self.get_absolute_pos() - shape.get_absolute_pos()
            if v.magnitude() == 0:
                return pg.math.Vector2(0,0)
            normal = v / v.magnitude()
            return normal * (velocity * normal) * (-2)
        if isinstance(shape, PlaneShape):
            return shape.normal * (velocity * shape.normal) * (-2)

    def collide_reflect_position(self, shape):
        if isinstance(shape, CircleShape):
            v = self.get_absolute_pos() - shape.get_absolute_pos()
            if v.magnitude() == 0:
                return pg.math.Vector2(0,0)
            normal = v / v.magnitude()
            if v.magnitude() - self.radius - shape.radius < 0:
                return (-1) * (v.magnitude() - self.radius - shape.radius) * normal
            else:
                return pg.math.Vector2(0, 0)
        if isinstance(shape, PlaneShape):
            dc = self.get_absolute_pos() * shape.normal
            d = shape.get_absolute_pos() * shape.normal
            if abs(d - dc) - self.radius < 0:
                return (-1) * (abs(d - dc) - self.radius) * shape.normal
            else:
                return pg.math.Vector2(0, 0)

    def collide_with(self, shape, velocity):
        if isinstance(shape, CircleShape):
            v = self.get_absolute_pos() - shape.get_absolute_pos()
            if v * v < (self.radius + shape.radius) ** 2 + TOLERANCE:
                if v * velocity > 0:
                    return True, False
                else:
                    return True, True
            else:
                return False, False
        elif isinstance(shape, PlaneShape):
            dc = self.get_absolute_pos() * shape.normal
            d = shape.get_absolute_pos() * shape.normal
            if abs(d - dc) < self.radius + TOLERANCE:
                if shape.normal * velocity > 0:
                    return True, False
                else:
                    return True, True
            else:
                return False, False
