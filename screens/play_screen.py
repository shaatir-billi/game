import pygame
import sys
from sprite import Sprite
from map import *
from camera import Camera
from utils.globals import *


def play(SCREEN):
    game_map = GameMap("assets/map/sky.jpeg",
                       "assets/map/ground.png")
    camera = Camera((SCREEN_WIDTH, SCREEN_HEIGHT), map_width)

    player = Sprite(
        sprite_sheet_path="assets/sprites/player/sprite_sheet.png",
        x=100,
        y=game_map.ground_level - 150,  # Adjust to spawn above the ground
        frame_width=32,
        frame_height=32,
        scale=5,
        ground_level=game_map.ground_level  # Pass ground level to the sprite
    )

    ground = game_map.ground_level

    d = False
    # Width:
    # 50 = 1 tile
    # 100 = 2 tiles and so on

    # Create platforms
    platforms = [

        # 2 tiles
        Platform("assets/map/platform.png", 2000, ground - 30, 100, 50),
        Platform("assets/map/platform.png", 2100, ground - 80, 100, 50),
        Platform("assets/map/platform.png", 2200, ground - 140, 100, 50),
        Platform("assets/map/platform.png", 1200, ground - 350, 100, 50),
        Platform("assets/map/platform.png", 1200, ground - 350, 100, 50),
        Platform("assets/map/platform.png", 3600, ground - 100, 100, 50),

        # 3 tiles
        Platform("assets/map/platform.png", 2300, ground - 250, 200, 50),
        Platform("assets/map/platform.png", 1600, ground - 630, 200, 50),
        Platform("assets/map/platform.png", 1900, ground - 630, 200, 50),
        Platform("assets/map/platform.png", 2700, ground - 550, 200, 50),
        Platform("assets/map/platform.png", 2580, ground - 100, 200, 50),


        # 4 tiles
        Platform("assets/map/platform.png", 1000, ground - 200, 250, 50),
        Platform("assets/map/platform.png", 2100, ground - 400, 250, 50),
        Platform("assets/map/platform.png", 3500, ground - 550, 250, 50),
        Platform("assets/map/platform.png", 2630, ground - 280, 250, 50),
        Platform("assets/map/platform.png", 3350, ground - 290, 250, 50),



        # Long platforms
        Platform("assets/map/platform.png", 1350, ground - 270, 800, 50),
        Platform("assets/map/platform.png", 700, ground - 400, 400, 50),
        Platform("assets/map/platform.png", 1000, ground - 550, 500, 50),
        Platform("assets/map/platform.png", 0, ground - 640, 900, 50),
        Platform("assets/map/platform.png", 2230, ground - 700, 1200, 50),
        Platform("assets/map/platform.png", 2900, ground - 200, 600, 50),
        Platform("assets/map/platform.png", 3000, ground - 460, 400, 50),


    ]

    # Wall at the 2500 division line.

    Walls = [

        Platform("assets/map/platform.png", 2500, 300, 50, 550),
    ]

    clock = pygame.time.Clock()

    # Add persistent horizontal velocity
    player.horizontal_velocity = 0

    while True:
        SCREEN.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # Update horizontal velocity only if keys are pressed
        if keys[pygame.K_a]:
            player.horizontal_velocity = -5
            player.set_animation(5)  # Walking animation
        elif keys[pygame.K_d]:
            player.horizontal_velocity = 5
            player.set_animation(5)  # Walking animation
        else:
            # Gradually stop horizontal movement on the ground
            if not player.is_jumping:
                player.horizontal_velocity = 0

        # Jump logic
        if keys[pygame.K_w]:
            player.jump()

        # Move player horizontally and apply gravity for vertical movement
        player.move(player.horizontal_velocity, 0)

        # Handle platform collision and falling
        on_platform = False
        for platform in platforms:
            # Check if the player is on top of the platform
            if (
                player.rect.colliderect(platform.rect)
                and player.y_velocity >= 0  # Falling or standing still
                and player.rect.bottom <= platform.rect.top + 20  # Slight overlap allowed
                # Within horizontal bounds
                and platform.rect.left <= player.rect.centerx <= platform.rect.right
            ):
                player.rect.bottom = platform.rect.top
                player.is_jumping = False
                player.y_velocity = 0
                on_platform = True
                break

        for wall in Walls:
            if player.rect.colliderect(wall.rect):
                overlap_left = wall.rect.right - player.rect.left
                overlap_right = player.rect.right - wall.rect.left
                # check if player is on the left side of the wall
                if abs(overlap_left) < abs(overlap_right):
                    player.rect.left = wall.rect.right
                # check if player is on the right side of the wall
                else:
                    player.rect.right = wall.rect.left

                # If the player is not on any platform, apply gravity
        if not on_platform and player.rect.bottom < game_map.ground_level:
            player.is_jumping = True

        player.update()

        camera.follow_sprite(player)
        game_map.draw(SCREEN, camera)

        for platform in platforms:
            platform.draw(SCREEN, camera)

        for wall in Walls:
            wall.draw(SCREEN, camera)

        player.draw(SCREEN, camera)

        pygame.display.flip()
        clock.tick(60)