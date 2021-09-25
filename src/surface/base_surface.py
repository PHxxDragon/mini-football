from typing import List
import pygame as pg


class BaseImage:
    def get_frame(self, now):
        pass


class NoAnimation(BaseImage):
    def __init__(self, frame):
        self.frame = frame

    def get_frame(self, now):
        return self.frame


class Animation(BaseImage):
    def __init__(self, frames, fps=24, loops=-1):
        self.fps = fps
        self.frame = 0
        self.loops = loops
        self.loop_count = 0
        self.frames = frames
        self.time = None
        self.done = False

    def reset(self):
        self.frame = 0
        self.loop_count = 0
        self.done = False
        self.time = None

    def get_frame(self, now):
        if not self.time:
            self.time = now
        if now - self.time > 1000.0 / self.fps:
            self.frame = (self.frame + 1) % len(self.frames)
            if self.frame == 0:
                self.loop_count += 1
                if self.loops != -1 and self.loop_count >= self.loops:
                    self.done = True
                    self.frame = (self.frame - 1) % len(self.frames)
            self.time = now
        return self.frames[self.frame]


class BaseSurface:
    DEFAULT_STATE = 0

    def __init__(self):
        self.states = [BaseSurface.DEFAULT_STATE]
        self.state = BaseSurface.DEFAULT_STATE
        self.images: List[BaseImage] = None
        self.surface = None

    def set_state(self, state):
        self.state = state

    def update(self, now):
        self.surface = self.images[self.state].get_frame(now)

    def get_surface(self) -> pg.Surface:
        return self.surface
