import pygame
import pygame as pg
from pygame.math import Vector2

from src.state.state_machine import State
from src.state.game.game_objects import Ball
from src.state.game.game_objects import Field
from src.state.game.game_objects import Team
from src.state.game.game_objects import Line
from src.physics.world import World


def get_move_direction(keyboard):
    direction = Vector2(0, 0)
    if keyboard[pygame.K_LEFT]:
        direction += Vector2(-1, 0)
    if keyboard[pygame.K_RIGHT]:
        direction += Vector2(1, 0)
    if keyboard[pygame.K_UP]:
        direction += Vector2(0, -1)
    if keyboard[pygame.K_DOWN]:
        direction += Vector2(0, 1)
    return direction


class Game(State):
    def __init__(self):
        super().__init__()
        self.name = "GAME"
        self.group_all = pg.sprite.Group()
        self.world = World()
        self.ball = Ball(self)
        self.team0 = Team(self, 0, 3)
        self.lines = [
            Line(self, direction=Line.LEFT),
            Line(self, direction=Line.RIGHT),
            Line(self, direction=Line.UP),
            Line(self, direction=Line.DOWN),
            ]
        self.field = Field(self)
        self.group_all.add(self.field)
        self.group_all.add(self.ball)
        self.group_all.add(self.team0.players)
        self.group_all.add(*self.lines)

    def startup(self, now, to_persist):
        self.world.apply_permanent_acceleration(Vector2(9.8, 0))

    def accept_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.team0.change_player()

    def update(self, now, mouse_pos, keyboard):
        self.team0.move_player(get_move_direction(keyboard))
        self.world.update(now)
        self.group_all.update(now)

    def draw(self, surface: pg.Surface, interpolate):
        self.group_all.draw(surface)
