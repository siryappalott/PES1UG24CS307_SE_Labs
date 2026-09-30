"""
GameEngine: owns the puck, paddles, AI, scoring, timer, and match state.
"""

import random

from game.puck import Puck
from game.paddle import Paddle
from game.ai import ComputerAI
from game.collisions import handle_paddle_collision
from game.renderer import WIDTH, HEIGHT, MARGIN, GOAL_TOP, GOAL_BOTTOM

PLAYER_SPEED = 6
PUCK_RADIUS = 12
PADDLE_RADIUS = 28
INITIAL_PUCK_SPEED = 4.5

MATCH_DURATION = 30.0
WINNING_SCORE = 5


class GameEngine:
    def __init__(self):
        self.player_score = 0
        self.computer_score = 0

        self.time_remaining = MATCH_DURATION

        self.game_over = False
        self.winner = None

        self.puck = Puck(WIDTH / 2, HEIGHT / 2, PUCK_RADIUS)

        self.player = Paddle(
            x=WIDTH * 0.15,
            y=HEIGHT / 2,
            radius=PADDLE_RADIUS,
            min_x=MARGIN + PADDLE_RADIUS,
            max_x=WIDTH / 2 - PADDLE_RADIUS,
            min_y=MARGIN + PADDLE_RADIUS,
            max_y=HEIGHT - MARGIN - PADDLE_RADIUS,
        )

        self.computer = Paddle(
            x=WIDTH * 0.85,
            y=HEIGHT / 2,
            radius=PADDLE_RADIUS,
            min_x=WIDTH / 2 + PADDLE_RADIUS,
            max_x=WIDTH - MARGIN - PADDLE_RADIUS,
            min_y=MARGIN + PADDLE_RADIUS,
            max_y=HEIGHT - MARGIN - PADDLE_RADIUS,
        )

        self.ai = ComputerAI()

        self._reset_puck()

    def _reset_puck(self):
        """
        Fully reset the puck after a goal.

        The position is always the exact centre and the velocity is always
        rebuilt from scratch. A non-zero random direction is selected so
        the puck can never remain stationary after a goal.
        """

        self.puck.x = WIDTH / 2
        self.puck.y = HEIGHT / 2

        angle_choices = (0.3, 0.6, -0.3, -0.6)
        direction = random.choice((-1, 1))
        vy_factor = random.choice(angle_choices)

        self.puck.vx = INITIAL_PUCK_SPEED * direction
        self.puck.vy = INITIAL_PUCK_SPEED * vy_factor

        # Defensive guarantee: never allow a zero-speed reset.
        if self.puck.vx == 0 and self.puck.vy == 0:
            self.puck.vx = INITIAL_PUCK_SPEED

    def handle_input(self, keys_pressed):
        if self.game_over:
            return

        import pygame

        dx = 0
        dy = 0

        if keys_pressed[pygame.K_UP]:
            dy -= PLAYER_SPEED
        if keys_pressed[pygame.K_DOWN]:
            dy += PLAYER_SPEED
        if keys_pressed[pygame.K_LEFT]:
            dx -= PLAYER_SPEED
        if keys_pressed[pygame.K_RIGHT]:
            dx += PLAYER_SPEED

        self.player.move_by(dx, dy)

    def update(self, dt):
        """
        Advance the game by dt seconds.

        The timer uses real elapsed time, so it is independent of FPS.
        """

        if self.game_over:
            return

        self.time_remaining = max(0.0, self.time_remaining - dt)

        if self.time_remaining <= 0.0:
            self._finish_by_time()
            return

        self.ai.update(self.computer, self.puck)

        previous_x = self.puck.x
        previous_y = self.puck.y

        self.puck.move()

        # Goals are checked before the end-wall bounce.
        if self._handle_goals(previous_x, previous_y):
            return

        self.puck.bounce_off_walls(HEIGHT, MARGIN)

        handle_paddle_collision(
            self.puck,
            self.player,
            previous_x,
            previous_y,
        )

        handle_paddle_collision(
            self.puck,
            self.computer,
            self.puck.x,
            self.puck.y,
        )

    def _handle_goals(self, previous_x, previous_y):
        """
        Score only when the entire puck passes through the goal opening.

        A wall hit outside the opening is a normal bounce.
        """

        fully_inside_goal_gap = (
            self.puck.y - self.puck.radius >= GOAL_TOP
            and self.puck.y + self.puck.radius <= GOAL_BOTTOM
        )

        # Left goal: computer scores.
        if self.puck.vx < 0 and self.puck.x + self.puck.radius < MARGIN:
            if fully_inside_goal_gap:
                self._score_point("computer")
            else:
                self.puck.x = MARGIN + self.puck.radius
                self.puck.vx = abs(self.puck.vx)

            return True if self.game_over else fully_inside_goal_gap

        # Right goal: player scores.
        if self.puck.vx > 0 and self.puck.x - self.puck.radius > WIDTH - MARGIN:
            if fully_inside_goal_gap:
                self._score_point("player")
            else:
                self.puck.x = WIDTH - MARGIN - self.puck.radius
                self.puck.vx = -abs(self.puck.vx)

            return True if self.game_over else fully_inside_goal_gap

        return False

    def _score_point(self, scorer):
        """Award a point and reset the puck into active play."""

        if scorer == "player":
            self.player_score += 1
        else:
            self.computer_score += 1

        if self.player_score >= WINNING_SCORE:
            self._finish_match("Player")
        elif self.computer_score >= WINNING_SCORE:
            self._finish_match("Computer")
        else:
            # Every goal gets a complete clean puck reset.
            self._reset_puck()

    def _finish_by_time(self):
        """Determine the result when the 30-second timer expires."""

        if self.player_score > self.computer_score:
            self._finish_match("Player")
        elif self.computer_score > self.player_score:
            self._finish_match("Computer")
        else:
            self._finish_match("Draw")

    def _finish_match(self, winner):
        """Freeze the match and store the final result."""

        self.game_over = True
        self.winner = winner
        self.time_remaining = 0.0

        self.puck.vx = 0.0
        self.puck.vy = 0.0

    def reset_match(self):
        """Reset the complete match."""

        self.player_score = 0
        self.computer_score = 0
        self.time_remaining = MATCH_DURATION
        self.game_over = False
        self.winner = None

        self._reset_puck()

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_table(surface)

        renderer.draw_paddle(
            surface,
            self.player,
            renderer.COLOR_PLAYER,
        )

        renderer.draw_paddle(
            surface,
            self.computer,
            renderer.COLOR_COMPUTER,
        )

        if not self.game_over:
            renderer.draw_puck(surface, self.puck)

        text_color = getattr(
            renderer,
            "COLOR_TEXT",
            (255, 255, 255),
        )

        # Score.
        player_text = font.render(
            f"PLAYER  {self.player_score}",
            True,
            renderer.COLOR_PLAYER,
        )

        computer_text = font.render(
            f"COMPUTER  {self.computer_score}",
            True,
            renderer.COLOR_COMPUTER,
        )

        surface.blit(
            player_text,
            (MARGIN + 20, 15),
        )

        computer_rect = computer_text.get_rect()
        computer_rect.top = 15
        computer_rect.right = WIDTH - MARGIN - 20
        surface.blit(computer_text, computer_rect)

        # Countdown.
        seconds_left = max(
            0,
            int(self.time_remaining + 0.999),
        )

        timer_text = font.render(
            str(seconds_left),
            True,
            text_color,
        )

        timer_rect = timer_text.get_rect(
            center=(WIDTH // 2, 28)
        )

        surface.blit(timer_text, timer_rect)

        # Final result.
        if self.game_over:
            background = getattr(
                renderer,
                "COLOR_BG",
                (20, 20, 20),
            )

            surface.fill(background)
            renderer.draw_table(surface)

            if self.winner == "Draw":
                result_text = "DRAW"
                result_color = text_color
            else:
                result_text = f"{self.winner.upper()} WINS!"
                result_color = (
                    renderer.COLOR_PLAYER
                    if self.winner == "Player"
                    else renderer.COLOR_COMPUTER
                )

            winner_text = font.render(
                result_text,
                True,
                result_color,
            )

            score_text = font.render(
                f"{self.player_score} - {self.computer_score}",
                True,
                text_color,
            )

            restart_text = font.render(
                "Press R to play again",
                True,
                text_color,
            )

            winner_rect = winner_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 - 35)
            )

            score_rect = score_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 5)
            )

            restart_rect = restart_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 45)
            )

            surface.blit(winner_text, winner_rect)
            surface.blit(score_text, score_rect)
            surface.blit(restart_text, restart_rect)
