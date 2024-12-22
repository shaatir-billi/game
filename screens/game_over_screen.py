import pygame
import sys
from utils.button import Button
from utils.font import get_font, draw_text_with_border
from utils.globals import SCREEN_WIDTH, SCREEN_HEIGHT


def game_over(SCREEN, play_function):
    clock = pygame.time.Clock()
    while True:
        SCREEN.fill("black")

        GAME_OVER_MOUSE_POS = pygame.mouse.get_pos()

        draw_text_with_border(
            SCREEN,
            "Game Over",
            get_font(70),
            text_color="#FF0000",  # Main text color
            border_color="#000000",  # Border color (black)
            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4),
            border_width=3  # Adjust border width
        )

        TRY_AGAIN_BUTTON = Button(
            image=pygame.image.load("assets/menu/play_button_rect.png"),
            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            text_input="TRY AGAIN",
            font=get_font(50),
            base_color="#000000",
            hovering_color="#FFFFFF",
        )
        QUIT_BUTTON = Button(
            image=pygame.image.load("assets/menu/play_button_rect.png"),
            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5),
            text_input="QUIT",
            font=get_font(50),
            base_color="#000000",
            hovering_color="#FFFFFF",
        )

        for button in [TRY_AGAIN_BUTTON, QUIT_BUTTON]:
            button.changeColor(GAME_OVER_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if TRY_AGAIN_BUTTON.checkForInput(GAME_OVER_MOUSE_POS):
                    play_function(SCREEN)
                if QUIT_BUTTON.checkForInput(GAME_OVER_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(60)
