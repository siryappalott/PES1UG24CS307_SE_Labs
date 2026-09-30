"""
Air Hockey

Run with:
    python3 main.py

Controls:
    Arrow keys - move the player paddle
    R          - restart after the match ends
"""

import pygame

from game.game_engine import GameEngine
from game.renderer import WINDOW_SIZE


def main():
    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Air Hockey")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 24)

    engine = GameEngine()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_r
                and engine.game_over
            ):
                engine.reset_match()

        keys = pygame.key.get_pressed()
        engine.handle_input(keys)

        # Real elapsed time in seconds.
        dt = clock.tick(60) / 1000.0

        engine.update(dt)
        engine.draw(screen, font)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
