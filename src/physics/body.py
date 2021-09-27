from typing import Set

import pygame as pg
from src.physics.world import DEFAULT_GROUP
from src.physics.world import DYNAMIC_BODY
from src.physics.world import KINEMATIC_BODY
from src.physics.world import STATIC_BODY
from src.common.config import METER_TO_PIXEL
from src.physics.shape import BaseShape


class Body:
    MAX_ID = 0

    def __init__(self, shape, body_type=DYNAMIC_BODY, mass=1.0, reduce_coefficient=0.9):
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
        self.reduce_coefficient = reduce_coefficient
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

    def set_velocity(self, velocity):
        self.velocity = pg.math.Vector2(velocity)

    def set_position(self, position):
        self.position = pg.math.Vector2(position)

    def get_position(self):
        return self.position

    def update(self, now):
        if self.previous_time == -1:
            self.previous_time = now
            return

        delta_time = (now - self.previous_time) / 1000.0
        if self.body_type == DYNAMIC_BODY:
            delta_time_divide_mass = delta_time / self.mass

            self.position += self.velocity * delta_time * METER_TO_PIXEL

            sum_force = pg.math.Vector2(0, 0)
            sum_force += self.instant_force + self.permanent_acceleration * self.mass
            for force, duration in self.temporary_forces:
                sum_force += force

            sum_force = self.check_collision_for_dynamic_body(sum_force)

            self.velocity += sum_force * delta_time_divide_mass

            new_temporary_forces = []
            for force, duration in self.temporary_forces:
                if duration > delta_time:
                    new_temporary_forces.append((force, duration - delta_time))
            self.temporary_forces = new_temporary_forces
            self.instant_force = pg.math.Vector2(0, 0)

        elif self.body_type == KINEMATIC_BODY:
            # self.velocity = self.check_collision_for_kinematic_body(self.velocity)
            self.position += self.velocity * delta_time * METER_TO_PIXEL
        self.previous_time = now

    def check_collision_for_kinematic_body(self, velocity):
        new_velocity = velocity
        for body in self.world.bodies[DEFAULT_GROUP].values():
            if body is not self:
                collide, not_away = self.shape.collide_with(body.shape, velocity)
                if collide and not_away:
                    reflection = \
                        self.shape.collide_reflect_velocity(body.shape, velocity)
                    velocity += reflection / 2
                    self.position += self.shape.collide_reflect_position(body.shape)

        return new_velocity

    def check_collision_for_dynamic_body(self, sum_force):
        for body in self.world.bodies[DEFAULT_GROUP].values():
            if body is not self:
                if body.body_type in [STATIC_BODY, KINEMATIC_BODY]:
                    collide, not_away = self.shape.collide_with(body.shape, self.velocity)
                    if collide:
                        reflection = \
                            self.shape.collide_reflect_velocity(body.shape, self.velocity - body.velocity)
                        self.position += self.shape.collide_reflect_position(body.shape)
                        if not_away:
                            self.velocity += reflection * self.reduce_coefficient * body.reduce_coefficient
                        else:
                            if reflection.magnitude() < 2:
                                self.velocity += reflection / 2
                                sum_force += self.shape.collide_reflect_force(body.shape, sum_force) / 2
                            else:
                                self.velocity += reflection * self.reduce_coefficient * body.reduce_coefficient
        return sum_force
