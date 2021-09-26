import pygame
import pygame as pg
from pygame.math import Vector2

from src.state.state_machine import State
from src.state.game.game_objects import Ball
from src.state.game.game_objects import Field
from src.state.game.game_objects import Team
from src.state.game.game_objects import Score
from src.state.game.game_objects import Goal
from src.state.game.game_objects import Border
from src.physics.world import World
from src.common.config import WIN_SCORE


def get_move_direction_0(keyboard):
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


def get_move_direction_1(keyboard):
    direction = Vector2(0, 0)
    if keyboard[pygame.K_a]:
        direction += Vector2(-1, 0)
    if keyboard[pygame.K_d]:
        direction += Vector2(1, 0)
    if keyboard[pygame.K_w]:
        direction += Vector2(0, -1)
    if keyboard[pygame.K_s]:
        direction += Vector2(0, 1)
    return direction


class Game(State):
    def __init__(self):
        super().__init__()
        self.name = "GAME"
        self.group_all = None
        self.world = None
        self.ball = None
        self.team0 = None
        self.team1 = None
        self.border = None
        self.goal1 = None
        self.goal0 = None
        self.score = None
        self.field = None
        self.reset()

    def reset(self):
        self.group_all = pg.sprite.Group()
        self.world = World()
        self.ball = Ball(self)
        self.team0 = Team(self, 0, 3)
        self.team1 = Team(self, 1, 3)
        self.border = Border(self)
        self.goal0 = Goal(self, 0)
        self.goal1 = Goal(self, 1)
        self.score = Score(self)
        self.field = Field(self)
        self.group_all.add(self.field)
        self.group_all.add(self.goal0)
        self.group_all.add(self.goal1)
        self.group_all.add(self.ball)
        self.group_all.add(self.border.lines)
        self.group_all.add(self.team0.players)
        self.group_all.add(self.team1.players)
        self.group_all.add(self.score)

    def game_score(self, team):
        if team == 0:
            self.score.update_score(team0=self.score.team0 + 1)
        else:
            self.score.update_score(team1=self.score.team1 + 1)
        self.persist['score'] = (self.score.team0, self.score.team1)
        if self.score.team0 == WIN_SCORE or self.score.team1 == WIN_SCORE:
            self.next_state_name = 'TITLE'
        else:
            self.next_state_name = 'COUNTDOWN'
        self.done = True

    def startup(self, now, to_persist):
        super().startup(now, to_persist)
        if 'score' in to_persist:
            self.score.update_score(*to_persist['score'])

    def cleanup(self):
        self.reset()
        return super().cleanup()

    def accept_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.team0.change_player()
                elif event.key == pygame.KMOD_RSHIFT:
                    self.team0.shoot()
                elif event.key == pygame.K_SPACE:
                    self.team1.shoot()
                elif event.key == pygame.K_x:
                    self.team1.change_player()

    def update(self, now, mouse_pos, keyboard):
        self.team1.move_player(get_move_direction_1(keyboard))
        self.team0.move_player(get_move_direction_0(keyboard))
        self.group_all.update(now)
        self.world.update(now)

    def draw(self, surface: pg.Surface, interpolate):
        self.group_all.draw(surface)
