import pygame as pg

from src.state.state_machine import State
from src.state.title.title_objects import Field
from src.state.title.title_objects import Score
from src.state.title.title_objects import PressKeyText


class TitleScreen(State):
    def __init__(self):
        super().__init__()
        self.name = "TITLE"
        self.next_state_name = "COUNTDOWN"
        self.field = Field(self)
        self.score = Score(self)
        self.press_key = PressKeyText(self)
        self.group_all = pg.sprite.Group()
        self.group_all.add(self.field)
        self.group_all.add(self.score)
        self.group_all.add(self.press_key)

    def startup(self, now, to_persist):
        super().startup(now, to_persist)
        if 'score' in to_persist:
            self.score.update_score(*to_persist['score'])
            self.persist.pop('score')

    def accept_events(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                self.done = True

    def update(self, now, mouse_pos, keyboard):
        self.group_all.update(now)

    def draw(self, surface, interpolate):
        self.group_all.draw(surface)
