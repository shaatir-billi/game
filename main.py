import pygame
from screens.main_menu import main_menu
from utils.globals import *

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

# Set up the screen
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shaatir Billi")

clock.tick(60)

# Run the main menu
main_menu(SCREEN)
