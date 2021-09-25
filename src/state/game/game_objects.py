import pygame as pg

from src.physics.body import Body
from src.surface.base_surface import BaseSurface
from src.surface.surfaces import BallSurface
from src.surface.surfaces import FieldSurface


class BaseSprite(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.surface: BaseSurface = None
        self.priority = 0

    def get_image(self):
        return self.surface.get_surface()

    def get_rect(self):
        pass

    def update(self, now):
        self.surface.update(now)

    # passing get_image and get_rect alone doesn't work with inheritance
    image = property(fget=lambda self: self.get_image())
    rect = property(fget=lambda self: self.get_rect())


class BasePhysicsSprite(BaseSprite):
    def __init__(self, game):
        super().__init__(game)
        self.body: Body = None

    def get_rect(self):
        return self.surface.get_surface().get_rect(center=self.body.get_position())


class Ball(BasePhysicsSprite):
    def __init__(self, game):
        super().__init__(game)
        self.surface = BallSurface()
        self.body = Body(Body.DYNAMIC_BODY)
        self.game.world.add_body(self.body)
        self.body.set_position((300, 300))


class Field(BaseSprite):
    def __init__(self, game):
        super().__init__(game)
        self.surface = FieldSurface()

    def get_rect(self):
        return self.surface.get_surface().get_rect(topleft=(0, 0))

