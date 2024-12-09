import pygame
import sys
from utils.button import Button
from map import GameMap
from sprite import Sprite
from camera import Camera
from utils.globals import *
from utils.font import *
import random

# Initialize pygame
pygame.init()

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shaatir Billi")

BG = pygame.image.load("assets/menu/background.jpeg")


# Game setup
game_map = GameMap(sky_image_path)
camera = Camera((SCREEN_WIDTH, SCREEN_HEIGHT), map_width)

player = Sprite(
    sprite_sheet_path="assets/sprites/player/sprite_sheet.png",
    x=100,
    y=300,
    frame_width=32,
    frame_height=32,
    scale=5
)

clock = pygame.time.Clock()

# Game loop


def play():
    while True:
        SCREEN.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pygame.K_a]:  # Move left
            dx = -5
            player.set_animation(5)
        if keys[pygame.K_d]:  # Move right
            dx = 5
            player.set_animation(5)
        if keys[pygame.K_SPACE]:  # Jump
            player.jump()

        player.move(dx, dy)
        player.update()

        camera.follow_sprite(player)
        game_map.draw(SCREEN, camera)
        player.draw(SCREEN, camera)

        pygame.display.flip()
        clock.tick(60)


def options():
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
                    main_menu()

        pygame.display.update()


def main_menu():
    # Scale the background image
    scaled_bg = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
    background_x = 0  # Initial horizontal position of the background
    scroll_speed = 4  # Speed at which the background scrolls

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

    jumping = False  # Flag to track if the sprite is jumping
    jump_velocity = -15  # Initial upward velocity for jumping
    gravity = 1  # Gravity value
    vertical_velocity = 0  # Current vertical velocity

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
            menu_sprite.move(-5, 0)
            menu_sprite.set_animation(5)  # Assuming 5 is the row for left
        elif sprite_timer == "right" and menu_sprite.rect.x < SCREEN_WIDTH - menu_sprite.rect.width:
            menu_sprite.move(5, 0)
            menu_sprite.set_animation(4)  # Assuming 4 is the row for right
        elif sprite_timer == "stop" and not jumping:
            menu_sprite.set_animation(0)  # Assuming 0 is the resting animation

        # Handle jumping and gravity
        if jumping:
            menu_sprite.move(0, vertical_velocity)
            vertical_velocity += gravity
            if menu_sprite.rect.y >= SCREEN_HEIGHT - 150:  # If sprite hits the ground
                menu_sprite.rect.y = SCREEN_HEIGHT - 150
                jumping = False
                vertical_velocity = 0

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
            border_width=2  # Adjust border width
        )

        PLAY_BUTTON = Button(
            image=None,
            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            text_input="PLAY",
            font=get_font(50),
            base_color="#FFFFFF",
            hovering_color="#FFD700",
        )
        OPTIONS_BUTTON = Button(
            image=None,
            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.7),
            text_input="OPTIONS",
            font=get_font(50),
            base_color="#FFFFFF",
            hovering_color="#FFD700",
        )
        QUIT_BUTTON = Button(
            image=None,
            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.4),
            text_input="QUIT",
            font=get_font(50),
            base_color="#FFFFFF",
            hovering_color="#FFD700",
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
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        # Update and draw the sprite
        menu_sprite.update()
        menu_sprite.draw(SCREEN, camera=Camera(
            (SCREEN_WIDTH, SCREEN_HEIGHT), map_width))

        pygame.display.update()
        clock.tick(60)


# Start the main menu
main_menu()
