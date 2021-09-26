import pygame as pg
from pygame.math import Vector2

from src.state.state_machine import State
from src.state.game.game_objects import Ball
from src.state.game.game_objects import Field
from src.state.game.game_objects import Line
from src.physics.world import World


class Game(State):
    def __init__(self):
        super().__init__()
        self.name = "GAME"
        self.group_all = pg.sprite.Group()
        self.world = World()
        self.ball = Ball(self)
        self.lines = [
            Line(self, direction=Line.LEFT),
            Line(self, direction=Line.RIGHT),
            Line(self, direction=Line.UP),
            Line(self, direction=Line.DOWN),
            ]
        self.field = Field(self)
        self.group_all.add(self.field)
        self.group_all.add(self.ball)
        self.group_all.add(*self.lines)

    def startup(self, now, to_persist):
        # self.world.apply_permanent_acceleration(Vector2(-49.8, -45))
        pass
    
    def accept_events(self, events):
        pass

    def update(self, now, mouse_pos, keyboard):
        self.world.update(now)
        self.group_all.update(now)

    def draw(self, surface: pg.Surface, interpolate):
        self.group_all.draw(surface)
