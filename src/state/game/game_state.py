import pygame as pg

from src.state.state_machine import State
from src.state.game.game_objects import Ball


class Game(State):
    def __init__(self):
        super().__init__()
        self.name = "GAME"
        self.group_all = pg.sprite.Group()
        self.ball = Ball(self)
        self.group_all.add(self.ball)

    def startup(self, now, to_persist):
        pass

    def accept_events(self, events):
        pass

    def update(self, now, mouse_pos):
        self.group_all.update(now)

    def draw(self, surface: pg.Surface, interpolate):
        self.group_all.draw(surface)
