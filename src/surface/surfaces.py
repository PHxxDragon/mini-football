import pygame as pg

from src.surface.base_surface import BaseSurface
from src.surface.base_surface import NoAnimation

from src.common.config import BALL_RADIUS
from src.common.config import SHOOT_RADIUS
from src.common.config import PLAYER_RADIUS
from src.common.config import GOAL_HEIGHT
from src.common.config import GOAL_WIDTH


class BallSurface(BaseSurface):
    def __init__(self):
        super().__init__()
        circle = pg.Surface((2*BALL_RADIUS, 2*BALL_RADIUS), pg.SRCALPHA)
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
    ACTIVE_STATE = 2

    def __init__(self, team):
        super().__init__()
        circle = pg.Surface((2 * PLAYER_RADIUS,2 * PLAYER_RADIUS), pg.SRCALPHA)
        active_circle = pg.Surface((2 * (PLAYER_RADIUS + SHOOT_RADIUS), 2 * (PLAYER_RADIUS + SHOOT_RADIUS)), pg.SRCALPHA)
        if team == 0:
            pg.draw.circle(circle, (255, 0, 0), (PLAYER_RADIUS, PLAYER_RADIUS), PLAYER_RADIUS)
            pg.draw.circle(active_circle, (100, 0, 0), (PLAYER_RADIUS + SHOOT_RADIUS, PLAYER_RADIUS + SHOOT_RADIUS),
                           PLAYER_RADIUS + SHOOT_RADIUS)
            pg.draw.circle(active_circle, (255, 0, 0), (PLAYER_RADIUS + SHOOT_RADIUS, PLAYER_RADIUS + SHOOT_RADIUS), PLAYER_RADIUS)
        else:
            pg.draw.circle(circle, (0, 0, 255), (PLAYER_RADIUS, PLAYER_RADIUS), PLAYER_RADIUS)
            pg.draw.circle(active_circle, (0, 0, 100), (PLAYER_RADIUS + SHOOT_RADIUS, PLAYER_RADIUS + SHOOT_RADIUS),
                           PLAYER_RADIUS + SHOOT_RADIUS)
            pg.draw.circle(active_circle, (0, 0, 255), (PLAYER_RADIUS + SHOOT_RADIUS, PLAYER_RADIUS + SHOOT_RADIUS),
                           PLAYER_RADIUS)
        self.images = {
            BaseSurface.DEFAULT_STATE: NoAnimation(circle),
            PlayerSurface.ACTIVE_STATE: NoAnimation(active_circle),
        }
        self.radius = PLAYER_RADIUS


class GoalSurface(BaseSurface):
    def __init__(self):
        super().__init__()
        rect_surface = pg.Surface((GOAL_WIDTH, GOAL_HEIGHT), pg.SRCALPHA)
        pg.draw.rect(rect_surface, (0, 90, 90), pg.rect.Rect(0, 0, GOAL_WIDTH, GOAL_HEIGHT))
        self.images = {
            BaseSurface.DEFAULT_STATE: NoAnimation(rect_surface)
        }


class TextSurface(BaseSurface):
    def __init__(self):
        super().__init__()
        self.font = pg.font.Font(None, 60)
        self.surface = None

    def set_text(self, text:str):
        self.surface = self.font.render(text, True, (255, 255, 255))

    def update(self, now):
        pass

    def get_surface(self) -> pg.Surface:
        return self.surface


