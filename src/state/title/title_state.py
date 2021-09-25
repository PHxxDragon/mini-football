import pygame as pg

from src.state.state_machine import State


class TitleScreen(State):
    def __init__(self):
        super().__init__()
        self.name = "TITLE"
        self.next_state_name = "GAME"

    def startup(self, now, to_persist):
        pass

    def accept_events(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                self.done = True

    def update(self, now, mouse_pos, keyboard):
        pass

    def draw(self, surface, interpolate):
        pass
