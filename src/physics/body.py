from typing import Set

import pygame as pg
from src.common.config import METER_TO_PIXEL


class Body:
    DYNAMIC_BODY = 0
    STATIC_BODY = 1
    KINEMATIC_BODY = 2
    MAX_ID = 0

    def __init__(self, body_type=DYNAMIC_BODY, mass=1.0):
        self.position = None
        self.shape = None
        self.body_type = body_type
        self.permanent_acceleration = pg.math.Vector2(0, 0)
        self.instant_force = pg.math.Vector2(0, 0)
        self.velocity = pg.math.Vector2(0, 0)
        self.mass = mass
        self.temporary_forces = []
        self.previous_time = 0.0    # in milliseconds
        self.groups: Set = set()
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
        delta_time = (now - self.previous_time) / 1000.0
        delta_time_divide_mass = delta_time / self.mass

        self.position += self.velocity * delta_time * METER_TO_PIXEL

        self.velocity += self.instant_force * delta_time_divide_mass + self.permanent_acceleration * delta_time

        new_temporary_forces = []
        sum_force = pg.math.Vector2(0, 0)
        for force, duration in self.temporary_forces:
            if duration < delta_time:
                self.velocity += force * duration / self.mass
            else:
                new_temporary_forces.append((force, duration - delta_time))
                sum_force += force
        self.velocity += sum_force * delta_time_divide_mass

        self.instant_force = pg.math.Vector2(0, 0)
        self.previous_time = now
