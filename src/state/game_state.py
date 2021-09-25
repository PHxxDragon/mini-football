import pygame as pg

from src.state.state_machine import State


class Game(State):
    def __init__(self):
        super().__init__()
        self.name = "GAME"

    def startup(self, now, to_persist):
        pass

    def accept_events(self, events):
        pass

    def update(self, now, mouse_pos):
        pass

    def draw(self, surface: pg.Surface, interpolate):
        pass
