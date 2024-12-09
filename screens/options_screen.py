import pygame
from utils.button import Button
from utils.font import get_font
from utils.globals import *
import sys


def options(SCREEN):
    while True:
        SCREEN.fill("white")

        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        OPTIONS_TEXT = get_font(45).render(
            "Options Placeholder", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(
            image=None,
            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5),
            text_input="BACK",
            font=get_font(50),
            base_color="Black",
            hovering_color="Green",
        )

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return  # Back to main menu

        pygame.display.update()
