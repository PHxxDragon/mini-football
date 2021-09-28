import pygame as pg
import os

from src.surface.base_surface import BaseSurface
from src.surface.base_surface import NoAnimation

from src.common.config import BALL_RADIUS
from src.common.config import SHOOT_RADIUS
from src.common.config import PLAYER_RADIUS
from src.common.config import GOAL_HEIGHT
from src.common.config import GOAL_WIDTH
from src.common.config import SCREEN_WIDTH
from src.common.config import SCREEN_HEIGHT


PROJECT_DIR = os.path.abspath(os.path.join(__file__, "..", "..", ".."))
RESOURCE_DIR = os.path.join(PROJECT_DIR, "resources")
_DEFAULT_COLOR_KEY = -1


_FIELD_IMAGE = None
_BALL_IMAGE = None
_PLAYER0_IMAGE = None
_PLAYER1_IMAGE = None
_PLAYER0_ACTIVE = None
_PLAYER1_ACTIVE = None


def load_image(name, alpha=False, color_key=None):
    file_path = os.path.join(RESOURCE_DIR, name)
    try:
        image = pg.image.load(file_path)
    except pg.error:
        print("Cannot load image: ", file_path)
        raise SystemExit(str(pg.compat.geterror()))
    if alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()
        if color_key is not None:
            if color_key == _DEFAULT_COLOR_KEY:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key, pg.RLEACCEL)
    return image


class BallSurface(BaseSurface):
    def __init__(self):
        super().__init__()
        global _BALL_IMAGE
        if _BALL_IMAGE is None:
            image_name = "ball.png"
            _BALL_IMAGE = load_image(image_name, alpha=True)
        image = _BALL_IMAGE
        image = pg.transform.scale(image, (2*BALL_RADIUS, 2*BALL_RADIUS))
        self.radius = BALL_RADIUS
        self.images = {
            BaseSurface.DEFAULT_STATE: NoAnimation(image)
        }


class FieldSurface(BaseSurface):
    def __init__(self):
        super().__init__()
        global _FIELD_IMAGE
        if _FIELD_IMAGE is None:
            image_name = "field_with_brick.png"
            _FIELD_IMAGE = load_image(image_name)
        image = _FIELD_IMAGE
        image = pg.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.images = {
            BaseSurface.DEFAULT_STATE: NoAnimation(image)
        }


class LineSurface(BaseSurface):
    def __init__(self, width, length):
        super().__init__()
        rect = pg.Surface((length, width), pg.SRCALPHA)
        rect.fill((0, 0, 0, 0))
        self.images = {
            BaseSurface.DEFAULT_STATE: NoAnimation(rect)
        }


class PlayerSurface(BaseSurface):
    ACTIVE_STATE = 2

    def __init__(self, team):
        super().__init__()
        if team == 0:
            global _PLAYER0_IMAGE
            if _PLAYER0_IMAGE is None:
                image_name = "player0.png"
                _PLAYER0_IMAGE = load_image(image_name, color_key=_DEFAULT_COLOR_KEY)
            image = _PLAYER0_IMAGE
            global _PLAYER0_ACTIVE
            if _PLAYER0_ACTIVE is None:
                image_name = "player0_active.png"
                _PLAYER0_ACTIVE = load_image(image_name, alpha=True)
            image_active = _PLAYER0_ACTIVE
        else:
            global _PLAYER1_IMAGE
            if _PLAYER1_IMAGE is None:
                image_name = "player1.png"
                _PLAYER1_IMAGE = load_image(image_name, color_key=_DEFAULT_COLOR_KEY)
                _PLAYER1_IMAGE = pg.transform.flip(_PLAYER1_IMAGE, True, False)
            image = _PLAYER1_IMAGE
            global _PLAYER1_ACTIVE
            if _PLAYER1_ACTIVE is None:
                image_name = "player1_active.png"
                _PLAYER1_ACTIVE = load_image(image_name, alpha=True)
            image_active = _PLAYER1_ACTIVE
        circle = image
        circle = pg.transform.scale(circle, (2 * PLAYER_RADIUS, 2 * PLAYER_RADIUS))
        active_circle = image_active
        active_radius = PLAYER_RADIUS + SHOOT_RADIUS
        active_circle = pg.transform.scale(active_circle, (2 * active_radius, 2 * active_radius))
        active_circle.blit(circle, circle.get_rect(center=(active_radius, active_radius)))
        self.images = {
            BaseSurface.DEFAULT_STATE: NoAnimation(circle),
            PlayerSurface.ACTIVE_STATE: NoAnimation(active_circle),
        }
        self.radius = PLAYER_RADIUS


class GoalSurface(BaseSurface):
    def __init__(self):
        super().__init__()
        rect_surface = pg.Surface((GOAL_WIDTH, GOAL_HEIGHT), pg.SRCALPHA)
        pg.draw.rect(rect_surface, (0, 90, 90, 0), pg.rect.Rect(0, 0, GOAL_WIDTH, GOAL_HEIGHT))
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


