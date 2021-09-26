import pygame as pg

from src.surface.base_surface import BaseSurface
from src.surface.base_surface import NoAnimation

from src.common.config import BALL_RADIUS


class BallSurface(BaseSurface):
    def __init__(self):
        super().__init__()
        circle = pg.Surface((2*BALL_RADIUS, 2*BALL_RADIUS))
        pg.draw.circle(circle, (0, 255, 0), (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.radius = BALL_RADIUS
        self.images = {
            BaseSurface.DEFAULT_STATE: NoAnimation(circle)
        }


class FieldSurface(BaseSurface):
    def __init__(self):
        super().__init__()
        green_rect = pg.Surface((1024, 614))
        green_rect.fill((20, 20, 20))
        self.images = {
            BaseSurface.DEFAULT_STATE: NoAnimation(green_rect)
        }


class LineSurface(BaseSurface):
    def __init__(self, width, length):
        super().__init__()
        rect = pg.Surface((length, width))
        rect.fill((0, 255, 0))
        self.images = {
            BaseSurface.DEFAULT_STATE: NoAnimation(rect)
        }


class PlayerSurface(BaseSurface):
    def __init__(self, team):
        super().__init__()
        circle = pg.Surface((64, 64))
        if team == 0:
            pg.draw.circle(circle, (255, 0, 0), (31, 31), 31)
        else:
            pg.draw.circle(circle, (0, 0, 255), (31, 31), 31)
        self.images = {
            BaseSurface.DEFAULT_STATE: NoAnimation(circle)
        }
