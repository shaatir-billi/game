import pygame
from utils.button import Button
from utils.font import get_font
from utils.globals import *
import sys


def how_to_play(SCREEN):
    how_to_play_image = pygame.image.load("assets/map/sky.jpeg")
    how_to_play_image = pygame.transform.scale(
        how_to_play_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    while True:
        SCREEN.fill("white")
        SCREEN.blit(how_to_play_image, (0, 0))

        HOW_TO_PLAY_MOUSE_POS = pygame.mouse.get_pos()

        BACK_BUTTON = Button(
            image=None,
            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.1),
            text_input="BACK",
            font=get_font(50),
            base_color="Black",
            hovering_color="Green",
        )

        BACK_BUTTON.changeColor(HOW_TO_PLAY_MOUSE_POS)
        BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(HOW_TO_PLAY_MOUSE_POS):
                    return  # Back to main menu

        pygame.display.update()
