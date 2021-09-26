from typing import Set

import pygame as pg
from src.physics.world import DEFAULT_GROUP
from src.common.config import METER_TO_PIXEL
from src.physics.shape import BaseShape


class Body:
    DYNAMIC_BODY = 0
    STATIC_BODY = 1
    KINEMATIC_BODY = 2
    MAX_ID = 0

    def __init__(self, shape, body_type=DYNAMIC_BODY, mass=1.0):
        self.position = pg.math.Vector2(0, 0)
        self.shape: BaseShape = shape
        shape.body = self
        self.body_type = body_type
        self.permanent_acceleration = pg.math.Vector2(0, 0)
        self.instant_force = pg.math.Vector2(0, 0)
        self.velocity = pg.math.Vector2(0, 0)
        self.mass = mass
        self.world = None
        self.temporary_forces = []
        self.previous_time = -1    # in milliseconds
        self.groups: Set = set()
        self.reduce_coefficient = 0.7
        Body.MAX_ID += 1
        self.id = Body.MAX_ID

    def apply_permanent_acceleration(self, acceleration: pg.math.Vector2):
        self.permanent_acceleration += acceleration

    def apply_temporary_force(self, force: pg.math.Vector2, duration):
        self.temporary_forces.append((force, duration))

    def apply_instant_force(self, force: pg.math.Vector2):
        self.instant_force += force

    def apply_impulse(self, impulse: pg.math.Vector2):
        self.velocity += impulse / self.mass

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def update(self, now):
        if self.previous_time == -1:
            self.previous_time = now
            return

        delta_time = (now - self.previous_time) / 1000.0
        if self.body_type == Body.DYNAMIC_BODY:
            delta_time_divide_mass = delta_time / self.mass

            self.position += self.velocity * delta_time * METER_TO_PIXEL

            sum_force = pg.math.Vector2(0, 0)
            sum_force += self.instant_force + self.permanent_acceleration * self.mass
            for force, duration in self.temporary_forces:
                sum_force += force

            sum_force = self.check_collision(sum_force)

            self.velocity += sum_force * delta_time_divide_mass

            new_temporary_forces = []
            for force, duration in self.temporary_forces:
                if duration > delta_time:
                    new_temporary_forces.append((force, duration - delta_time))
            self.temporary_forces = new_temporary_forces
            self.instant_force = pg.math.Vector2(0, 0)

        self.previous_time = now

    def check_collision(self, sum_force):
        for body in self.world.bodies[DEFAULT_GROUP].values():
            if body is not self:
                collide, away = self.shape.collide_with(body.shape, self.velocity)
                if collide and away:
                    reflection = \
                        self.shape.collide_reflect_velocity(body.shape, self.velocity)
                    if reflection.magnitude() > 2:
                        self.velocity += reflection * self.reduce_coefficient
                    else:
                        self.velocity += reflection / 2
                    self.position -= 2 * self.shape.collide_reflect_position(body.shape) * self.reduce_coefficient

                    sum_force = self.shape.collide_remain_force(body.shape, sum_force)
        return sum_force
