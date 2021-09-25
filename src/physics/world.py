import pygame as pg

from src.physics.body import Body


class World:
    DEFAULT_GROUP = "all"

    def __init__(self):
        self.bodies = {World.DEFAULT_GROUP: {}}

    def add_body(self, body: Body, *groups):
        self.bodies[World.DEFAULT_GROUP][body.id] = body
        for group in groups:
            if group is not World.DEFAULT_GROUP:
                if group not in self.bodies:
                    self.bodies[group] = {}
                self.bodies[group][body.id] = body
                body.groups.add(group)

    def remove_body(self, body: Body, *groups):
        if len(groups) != 0:
            for group in groups:
                if group is not World.DEFAULT_GROUP:
                    if group in self.bodies:
                        self.bodies[group].pop(body.id, None)
                        body.groups.discard(group)
            if len(body.groups) == 0:
                self.bodies[World.DEFAULT_GROUP].pop(body.id, None)
        else:
            for group in self.bodies:
                self.bodies[group].pop(body.id, None)
            body.groups.clear()

    def apply_permanent_acceleration(self, force: pg.math.Vector2, *groups):
        if len(groups) != 0:
            for group in groups:
                for body in self.bodies[group].values():
                    body.apply_permanent_acceleration(force)
        else:
            for body in self.bodies[World.DEFAULT_GROUP].values():
                body.apply_permanent_acceleration(force)

    def apply_instant_force(self, force: pg.math.Vector2, *groups):
        if len(groups) != 0:
            for group in groups:
                for body in self.bodies[group].values():
                    body.apply_instant_force(force)
        else:
            for body in self.bodies[World.DEFAULT_GROUP].values():
                body.apply_permanent_acceleration(force)

    def apply_temporary_force(self, force: pg.math.Vector2, *groups):
        if len(groups) != 0:
            for group in groups:
                for body in self.bodies[group].values():
                    body.apply_temporary_force(force)
        else:
            for body in self.bodies[World.DEFAULT_GROUP].values():
                body.apply_permanent_acceleration(force)

    def update(self, now):
        for body in self.bodies[World.DEFAULT_GROUP].values():
            body.update(now)
