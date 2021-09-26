import pygame as pg

DEFAULT_GROUP = "all"
DYNAMIC_BODY = 0
STATIC_BODY = 1
KINEMATIC_BODY = 2


class World:
    def __init__(self):
        self.bodies = {DEFAULT_GROUP: {}}

    def add_body(self, body, *groups):
        self.bodies[DEFAULT_GROUP][body.id] = body
        body.world = self
        for group in groups:
            if group is not DEFAULT_GROUP:
                if group not in self.bodies:
                    self.bodies[group] = {}
                self.bodies[group][body.id] = body
                body.groups.add(group)

    def remove_body(self, body, *groups):
        body.world = None
        if len(groups) != 0:
            for group in groups:
                if group is not DEFAULT_GROUP:
                    if group in self.bodies:
                        self.bodies[group].pop(body.id, None)
                        body.groups.discard(group)
            if len(body.groups) == 0:
                self.bodies[DEFAULT_GROUP].pop(body.id, None)
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
            for body in self.bodies[DEFAULT_GROUP].values():
                body.apply_permanent_acceleration(force)

    def apply_instant_force(self, force: pg.math.Vector2, *groups):
        if len(groups) != 0:
            for group in groups:
                for body in self.bodies[group].values():
                    body.apply_instant_force(force)
        else:
            for body in self.bodies[DEFAULT_GROUP].values():
                body.apply_permanent_acceleration(force)

    def apply_temporary_force(self, force: pg.math.Vector2, *groups):
        if len(groups) != 0:
            for group in groups:
                for body in self.bodies[group].values():
                    body.apply_temporary_force(force)
        else:
            for body in self.bodies[DEFAULT_GROUP].values():
                body.apply_permanent_acceleration(force)

    def update(self, now):
        for body in self.bodies[DEFAULT_GROUP].values():
            if body.body_type == KINEMATIC_BODY:
                body.update(now)
        for body in self.bodies[DEFAULT_GROUP].values():
            if body.body_type == DYNAMIC_BODY:
                body.update(now)
