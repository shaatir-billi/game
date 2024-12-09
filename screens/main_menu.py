import pygame
from utils.button import Button
from utils.font import get_font, draw_text_with_border
from screens.play_screen import play
from screens.options_screen import options
from utils.globals import SCREEN_WIDTH, SCREEN_HEIGHT
from sprite import Sprite
import random
from camera import Camera  # Import Camera class
import sys


def main_menu(SCREEN):
    clock = pygame.time.Clock()
    # Scale the background image
    BG = pygame.image.load("assets/menu/background.jpeg")
    scaled_bg = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
    background_x = 0  # Initial horizontal position of the background
    scroll_speed = 2  # Speed at which the background scrolls

    # Create the sprite for the main menu
    menu_sprite = Sprite(
        sprite_sheet_path="assets/sprites/player/sprite_sheet.png",
        x=SCREEN_WIDTH // 2,
        y=SCREEN_HEIGHT - 150,  # Ground level
        frame_width=32,
        frame_height=32,
        scale=5,
    )

    sprite_timer = 0  # Timer to control random actions
    sprite_action_interval = 1000  # Time in milliseconds between actions
    last_sprite_action_time = pygame.time.get_ticks()

    camera = Camera((SCREEN_WIDTH, SCREEN_HEIGHT), 2000)

    while True:
        # Scroll the background
        background_x -= scroll_speed
        if background_x <= -SCREEN_WIDTH:
            background_x = 0

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Randomly move the sprite
        current_time = pygame.time.get_ticks()
        if current_time - last_sprite_action_time > sprite_action_interval:
            sprite_timer = random.choice(["left", "right", "jump", "stop"])
            last_sprite_action_time = current_time

        if sprite_timer == "left" and menu_sprite.rect.x > 0:  # Move left only if not at the screen's left edge
            menu_sprite.move(-2, 0)
            menu_sprite.set_animation(5)  # Assuming 5 is the row for left
        elif sprite_timer == "right" and menu_sprite.rect.x < SCREEN_WIDTH - menu_sprite.rect.width:
            menu_sprite.move(2, 0)
            menu_sprite.set_animation(4)  # Assuming 4 is the row for right
        elif sprite_timer == "stop":
            menu_sprite.set_animation(0)  # Assuming 0 is the resting animation

        # Keep the sprite within horizontal bounds
        if menu_sprite.rect.x < 0:
            menu_sprite.rect.x = 0
        elif menu_sprite.rect.x > SCREEN_WIDTH - menu_sprite.rect.width:
            menu_sprite.rect.x = SCREEN_WIDTH - menu_sprite.rect.width

        # Draw the scrolling background
        SCREEN.blit(scaled_bg, (background_x, 0))
        SCREEN.blit(scaled_bg, (background_x + SCREEN_WIDTH, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        draw_text_with_border(
            SCREEN,
            "Shaatir Billi",
            get_font(70),
            text_color="#FFD700",  # Main text color
            border_color="#000000",  # Border color (black)
            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5),
            border_width=3  # Adjust border width
        )

        # Draw the subtitle with a border
        draw_text_with_border(
            SCREEN,
            "The Purr-fect Adventure!",
            get_font(30),
            text_color="#FFFFFF",  # Main text color
            border_color="#000000",  # Border color (black)
            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3.5),
            border_width=3  # Adjust border width
        )

        PLAY_BUTTON = Button(
            image=pygame.image.load("assets/menu/play_button_rect.png"),
            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            text_input="PLAY",
            font=get_font(50),
            base_color="#000000",
            hovering_color="#FFFFFF",
        )
        OPTIONS_BUTTON = Button(
            image=pygame.image.load("assets/menu/play_button_rect.png"),
            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.6),
            text_input="OPTIONS",
            font=get_font(50),
            base_color="#000000",
            hovering_color="#FFFFFF",
        )
        QUIT_BUTTON = Button(
            image=pygame.image.load("assets/menu/play_button_rect.png"),
            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.3),
            text_input="QUIT",
            font=get_font(50),
            base_color="#000000",
            hovering_color="#FFFFFF",
        )

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # Check button interactions
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(SCREEN)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options(SCREEN)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        # Update and draw the sprite
        menu_sprite.update()
        menu_sprite.draw(SCREEN, camera)

        pygame.display.update()
        clock.tick(180)
