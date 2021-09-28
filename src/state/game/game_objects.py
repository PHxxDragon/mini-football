import pygame as pg

from src.physics.body import Body
from src.surface.base_surface import BaseSurface
from src.surface.surfaces import BallSurface
from src.surface.surfaces import FieldSurface
from src.surface.surfaces import LineSurface
from src.surface.surfaces import PlayerSurface
from src.surface.surfaces import GoalSurface
from src.surface.surfaces import TextSurface
from src.physics.world import STATIC_BODY
from src.physics.world import KINEMATIC_BODY
from src.physics.world import DYNAMIC_BODY
from src.physics.shape import CircleShape
from src.physics.shape import PlaneShape
from src.common.config import LINE_WIDTH
from src.common.config import SCREEN_WIDTH
from src.common.config import SCREEN_HEIGHT
from src.common.config import PLAYER_SPEED
from src.common.config import SHOOT_RADIUS
from src.common.config import SHOOT_IMPULSE
from src.common.config import GOAL_HEIGHT
from src.common.config import TEAM_CONFIG


class BaseSprite(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.surface: BaseSurface = None
        self.priority = 0

    def set_rotation(self, rotation):
        self.surface.rotate(rotation)

    def get_image(self):
        return self.surface.get_surface()

    def get_rect(self):
        pass

    def update(self, now):
        self.surface.update(now)

    # passing get_image and get_rect alone doesn't work with inheritance
    image = property(fget=lambda self: self.get_image())
    rect = property(fget=lambda self: self.get_rect())


class BasePhysicsSprite(BaseSprite):
    def __init__(self, game):
        super().__init__(game)
        self.body: Body = None

    def get_rect(self):
        return self.surface.get_surface().get_rect(center=self.body.get_position())


class Line(BasePhysicsSprite):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (1, 0)
    RIGHT = (-1, 0)

    def __init__(self, game, width, length, position, direction=LEFT):
        super().__init__(game)
        self.body = Body(PlaneShape(pg.math.Vector2(direction), pg.math.Vector2(direction) * (LINE_WIDTH / 2), length=length), STATIC_BODY,
                         reduce_coefficient=1)
        self.game.world.add_body(self.body)
        self.surface = LineSurface(width, length)
        self.body.set_position(position)
        if direction in [Line.LEFT, Line.RIGHT]:
            self.set_rotation(90)


class Border:
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.up = Line(game, LINE_WIDTH, SCREEN_WIDTH, (SCREEN_WIDTH / 2, LINE_WIDTH / 2),
                       direction=Line.UP)
        self.down = Line(game, LINE_WIDTH, SCREEN_WIDTH, (SCREEN_WIDTH / 2, SCREEN_HEIGHT - LINE_WIDTH / 2),
                         direction=Line.DOWN)

        self.up_left = Line(game, LINE_WIDTH, (SCREEN_HEIGHT - GOAL_HEIGHT) / 2,
                            (LINE_WIDTH / 2, (SCREEN_HEIGHT - GOAL_HEIGHT) / 4), direction=Line.LEFT)
        self.down_left = Line(game, LINE_WIDTH, (SCREEN_HEIGHT - GOAL_HEIGHT) / 2,
                              (LINE_WIDTH / 2, SCREEN_HEIGHT - (SCREEN_HEIGHT - GOAL_HEIGHT) / 4),
                              direction=Line.LEFT)

        self.up_right = Line(game, LINE_WIDTH, (SCREEN_HEIGHT - GOAL_HEIGHT) / 2,
                             (SCREEN_WIDTH - LINE_WIDTH/2, (SCREEN_HEIGHT - GOAL_HEIGHT) / 4),
                             direction=Line.RIGHT)
        self.down_right = Line(game, LINE_WIDTH, (SCREEN_HEIGHT - GOAL_HEIGHT) / 2,
                               (SCREEN_WIDTH - LINE_WIDTH/2,
                                SCREEN_HEIGHT - (SCREEN_HEIGHT - GOAL_HEIGHT) / 4),
                               direction=Line.RIGHT)

        self.lines = (self.up, self.down, self.up_left, self.down_left, self.up_right, self.down_right)


class Ball(BasePhysicsSprite):
    def __init__(self, game):
        super().__init__(game)
        self.surface = BallSurface()
        self.body = Body(CircleShape(self.surface.radius), DYNAMIC_BODY)
        self.game.world.add_body(self.body)
        self.body.set_position((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))


class Field(BaseSprite):
    def __init__(self, game):
        super().__init__(game)
        self.surface = FieldSurface()

    def get_rect(self):
        return self.surface.get_surface().get_rect(topleft=(0, 0))


class Player(BasePhysicsSprite):
    def __init__(self, game, team):
        super().__init__(game)
        self.surface = PlayerSurface(team)
        self.body = Body(CircleShape(self.surface.radius), KINEMATIC_BODY, reduce_coefficient=0.8)
        self.game.world.add_body(self.body)
        self.body.set_position((100, 100))

    def set_position(self, position):
        self.body.set_position(position)

    def get_position(self):
        return self.body.get_position()

    def apply_velocity(self, velocity):
        self.body.set_velocity(velocity * self.body.mass * PLAYER_SPEED)

    def shoot(self):
        ball = self.game.ball
        if (
                ball.body.get_position() - self.body.get_position()).magnitude() < self.body.shape.radius + ball.body.shape.radius + SHOOT_RADIUS:
            direction = ball.body.get_position() - self.body.get_position()
            direction = direction / direction.magnitude()
            ball.body.apply_impulse(SHOOT_IMPULSE * direction)

    def set_state(self, state):
        self.surface.set_state(state)


class PlayerGroup:
    def __init__(self, game, team, num_player, spacing, x_range, y_range):
        x_range = pg.math.Vector2(x_range)
        y_range = pg.math.Vector2(y_range)
        self.game = game
        self.players = [Player(game, team) for i in range(num_player)]
        self.x_range = x_range
        self.y_range = y_range
        x_pos = (x_range.x + x_range.y)/2
        y_pos = (y_range.x + y_range.y)/2
        mid = (num_player - 1) / 2.0
        for i in range(num_player):
            new_y_pos = y_pos + (i - mid) * spacing
            self.players[i].set_position((x_pos, new_y_pos))

    def apply_velocity(self, direction):
        if direction.x != 0:
            if self.players[0].get_position().x - self.players[0].surface.radius < self.x_range.x and direction.x < 0\
                    or self.players[0].get_position().x + self.players[0].surface.radius > self.x_range.y and direction.x > 0:
                direction.x = 0
        if direction.y != 0:
            if self.players[0].get_position().y - self.players[0].surface.radius < self.y_range.x and direction.y < 0 \
                    or self.players[-1].get_position().y + self.players[-1].surface.radius > self.y_range.y and direction.y > 0:
                direction.y = 0
        for player in self.players:
            player.apply_velocity(direction)

    def shoot(self):
        for player in self.players:
            player.shoot()

    def set_state(self, state):
        for player in self.players:
            player.set_state(state)


class Team:
    def __init__(self, game, team):
        super().__init__()
        self.game = game
        self.player_groups = [PlayerGroup(game, team, *config) for config in TEAM_CONFIG[team]]
        self.current_player = 0
        self.player_groups[self.current_player].set_state(PlayerSurface.ACTIVE_STATE)
        self.players = [player for player_group in self.player_groups for player in player_group.players]

    def change_player(self, increase):
        self.player_groups[self.current_player].apply_velocity(pg.math.Vector2(0, 0))
        self.player_groups[self.current_player].set_state(BaseSurface.DEFAULT_STATE)
        self.current_player = self.current_player + increase
        self.current_player = self.current_player % len(self.player_groups)
        self.player_groups[self.current_player].set_state(PlayerSurface.ACTIVE_STATE)

    def move_player(self, direction):
        self.player_groups[self.current_player].apply_velocity(direction)

    def shoot(self):
        self.player_groups[self.current_player].shoot()


class Goal(BaseSprite):
    def __init__(self, game, team):
        super().__init__(game)
        self.surface = GoalSurface()
        self.team = team
        if self.team == 1:
            self.surface.rotate(180)

    def get_rect(self):
        if self.team == 0:
            return self.surface.get_surface().get_rect(midleft=(0, SCREEN_HEIGHT / 2))
        elif self.team == 1:
            return self.surface.get_surface().get_rect(midright=(SCREEN_WIDTH, SCREEN_HEIGHT / 2))

    def update(self, now):
        super().update(now)
        ball = self.game.ball
        if pg.math.Vector2(ball.body.get_position()).x < 0 and self.team == 0:
            self.game.game_score(1)
        elif pg.math.Vector2(ball.body.get_position()).x > SCREEN_WIDTH and self.team == 1:
            self.game.game_score(0)


class Score(BaseSprite):
    def __init__(self, game):
        super().__init__(game)
        self.team0 = 0
        self.team1 = 0
        self.surface = TextSurface()
        self.surface.set_text(str(self.team0) + " | " + str(self.team1))

    def update_score(self, team0 = None, team1 = None):
        if team0 is not None:
            self.team0 = team0
        if team1 is not None:
            self.team1 = team1
        self.surface.set_text(str(self.team0) + " | " + str(self.team1))

    def get_rect(self):
        return self.surface.get_surface().get_rect(midtop=(SCREEN_WIDTH/2, 0))

