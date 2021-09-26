from src.state.state_machine import State
import pygame as pg

from src.state.countdown.countdown_objects import CountDownText
from src.state.countdown.countdown_objects import Score
from src.state.countdown.countdown_objects import Field


class CountDown(State):
    def __init__(self):
        super().__init__()
        self.name = "COUNTDOWN"
        self.count = CountDownText(self, 2)
        self.field = Field(self)
        self.score = Score(self)
        self.next_state_name = "GAME"
        self.group_all = pg.sprite.Group()
        self.group_all.add(self.field)
        self.group_all.add(self.score)
        self.group_all.add(self.count)

    def startup(self, now, to_persist):
        super().startup(now, to_persist)
        if 'score' in to_persist:
            self.score.update_score(*to_persist['score'])

    def cleanup(self):
        self.count.kill()
        self.score.kill()
        self.count = CountDownText(self, 2)
        self.score = Score(self)
        self.group_all.add(self.count)
        self.group_all.add(self.score)
        return super().cleanup()

    def update(self, now, mouse_pos, keyboard):
        self.group_all.update(now)

    def draw(self, surface: pg.Surface, interpolate):
        self.group_all.draw(surface)
