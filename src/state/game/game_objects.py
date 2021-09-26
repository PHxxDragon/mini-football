import pygame as pg

from src.physics.body import Body
from src.surface.base_surface import BaseSurface
from src.surface.surfaces import BallSurface
from src.surface.surfaces import FieldSurface
from src.surface.surfaces import LineSurface
from src.physics.shape import CircleShape
from src.physics.shape import PlaneShape
from src.common.config import LINE_WIDTH
from src.common.config import SCREEN_WIDTH
from src.common.config import SCREEN_HEIGHT


class BaseSprite(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.surface: BaseSurface = None
        self.priority = 0

    def set_rotation(self, rotation):
        self.surface.rotate(rotation)

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


class Line(BasePhysicsSprite):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def __init__(self, game, direction=LEFT):
        super().__init__(game)
        self.body = Body(PlaneShape(pg.math.Vector2(direction), pg.math.Vector2(direction)), Body.STATIC_BODY)
        self.game.world.add_body(self.body)
        if direction == Line.LEFT:
            self.surface = LineSurface(LINE_WIDTH, SCREEN_HEIGHT - LINE_WIDTH)
            self.body.set_position((SCREEN_WIDTH - LINE_WIDTH, SCREEN_HEIGHT/2))
            self.set_rotation(90)
        elif direction == Line.RIGHT:
            self.surface = LineSurface(LINE_WIDTH, SCREEN_HEIGHT - LINE_WIDTH)
            self.body.set_position((LINE_WIDTH, SCREEN_HEIGHT/2))
            self.set_rotation(90)
        elif direction == Line.UP:
            self.surface = LineSurface(LINE_WIDTH, SCREEN_WIDTH - LINE_WIDTH)
            self.body.set_position((SCREEN_WIDTH/2, LINE_WIDTH))
        elif direction == Line.DOWN:
            self.surface = LineSurface(LINE_WIDTH, SCREEN_WIDTH - LINE_WIDTH)
            self.body.set_position((SCREEN_WIDTH/2, SCREEN_HEIGHT - LINE_WIDTH))


class Ball(BasePhysicsSprite):
    def __init__(self, game):
        super().__init__(game)
        self.surface = BallSurface()
        self.body = Body(CircleShape(self.surface.radius), Body.DYNAMIC_BODY)
        self.game.world.add_body(self.body)
        self.body.set_position((300, 300))


class Field(BaseSprite):
    def __init__(self, game):
        super().__init__(game)
        self.surface = FieldSurface()

    def get_rect(self):
        return self.surface.get_surface().get_rect(topleft=(0, 0))

