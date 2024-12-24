import pygame
import sys
from sprite import Sprite
from map import *
from camera import Camera
from utils.globals import *
from guard import Guard
from shopkeeper import Shopkeeper
from fish import Fish
from hiding_spot import HidingSpot
import random
from screens.game_over_screen import game_over


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

    Guards = [
        Guard("assets/sprites/guard/girl_walk.png",
              platforms[16].rect, 48, 48, 3.5),
        # Example guard on a long platform
        Guard("assets/sprites/guard/girl_walk.png",
              platforms[15].rect, 48, 48, 3.5)
    ]

    hiding_spots = [
        # Specify the platform index, the position on the platform, and the scale
        (16, 80, 1),  # Platform index 16, 80 pixels from the left, scale 3
        (2, 30, 1),  # Platform index 2, 30 pixels from the left, scale 2
        (5, 50, 1),  # Platform index 5, 50 pixels from the left, scale 2.5
        # Add more hiding spots as needed
    ]

    hiding_spot_objects = [
        HidingSpot(platforms[index].rect.x + offset,
                   platforms[index].rect.y - 50, 50, 50, scale)
        for index, offset, scale in hiding_spots
    ]

    # Add the shopkeeper on the opposite side of the wall
    shopkeeper = Shopkeeper(
        sprite_sheet_path="assets/sprites/shopkeeper/man_walk.png",
        ground_rect=pygame.Rect(
            Walls[0].rect.right + 200, Walls[0].rect.top, 600, Walls[0].rect.height),
        frame_width=48,
        frame_height=48,
        scale=3.5
    )

    # Add the fish
    fish = Fish(
        sprite_sheet_path="assets/sprites/fish/fish.png",
        frame_width=260,
        frame_height=110,
        scale=0.5  # Adjust scale to make fish smaller
    )

    fish_picked_up = False

    clock = pygame.time.Clock()

    # Add persistent horizontal velocity
    player.horizontal_velocity = 0

    health_display = []

    def create_health_display():
        for i in range(player.health):
            heart = pygame.image.load('assets/menu/Grass1.png').convert_alpha()
            heart_rect = heart.get_rect(topleft=(20 + i * 30, 20))
            health_display.append((heart, heart_rect))

    def update_health_display():
        for i, (heart, heart_rect) in enumerate(health_display):
            heart_rect.topleft = (20 + i * 30, 20)
            if i < player.health:
                heart.set_alpha(255)
            else:
                heart.set_alpha(0)

    create_health_display()

    hiding_cooldown = 500  # Cooldown period in milliseconds
    last_hiding_time = 0
    current_hiding_spot = None  # Track the current hiding spot

    def handle_guard_collision():
        if not player.is_invincible:
            for guard in Guards:
                if player.collision_rect.colliderect(guard.collision_rect):
                    # Check if the player is above the guard
                    if player.rect.bottom <= guard.rect.top + 10:
                        # Player is above the guard, no damage taken
                        continue
                    player.take_damage()
                    update_health_display()

    def handle_hiding():
        nonlocal last_hiding_time, current_hiding_spot
        current_time = pygame.time.get_ticks()
        if current_time - last_hiding_time > hiding_cooldown:
            for spot in hiding_spot_objects:
                if player.rect.colliderect(spot.rect):
                    if keys[pygame.K_e]:
                        if player.is_hidden:
                            player.unhide()
                            current_hiding_spot = None
                        else:
                            player.hide()
                            current_hiding_spot = spot
                        last_hiding_time = current_time

    while True:
        SCREEN.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # # Guards logic
        # for guard in Guards:
        #     guard.update()
        #     guard.move(guard.horizontal_velocity, 0)  # Move guard

        #     # Change direction slightly before reaching the platform's edge
        #     if guard.rect.right >= guard.platform_rect.right - 30:
        #         guard.rect.right = guard.platform_rect.right - 100
        #         guard.horizontal_velocity = -1  # Change direction to left
        #     elif guard.rect.left <= guard.platform_rect.left + 30:
        #         guard.rect.left = guard.platform_rect.left + 100
        #         guard.horizontal_velocity = 1  # Change direction to right

        #     if player.collision_rect.colliderect(guard.collision_rect):
        #         handle_guard_collision()
        # Initialize a dictionary to store distance_traveled for each guard
        distance_traveled = {guard: 0 for guard in Guards}

        keys = pygame.key.get_pressed()

        # Guards logic

        for guard in Guards:
            guard.update()
            guard.move(guard.horizontal_velocity, 0)  # Move guard

            # Update the distance traveled for this guard
            distance_traveled[guard] += abs(guard.horizontal_velocity)

            # Change direction near platform edges
            if guard.rect.right >= guard.platform_rect.right - 30:
                guard.rect.right = guard.platform_rect.right - 31
                guard.horizontal_velocity = -1  # Reverse direction
                # Reset distance after direction change
                distance_traveled[guard] = 0
            elif guard.rect.left <= guard.platform_rect.left + 30:
                guard.rect.left = guard.platform_rect.left + 31
                guard.horizontal_velocity = 1  # Reverse direction
                # Reset distance after direction change
                distance_traveled[guard] = 0

            # Collision detection with player
            if player.collision_rect.colliderect(guard.collision_rect):
                handle_guard_collision()

        # Handle guard collision
        handle_guard_collision()

        # Shopkeeper logic
        shopkeeper.update()
        shopkeeper.move(shopkeeper.horizontal_velocity, 0)  # Move shopkeeper

        # Change direction slightly before reaching the ground's edge
        if shopkeeper.rect.right >= shopkeeper.ground_rect.right - 30:
            shopkeeper.rect.right = shopkeeper.ground_rect.right - 100
            shopkeeper.horizontal_velocity = -1  # Change direction to left
        elif shopkeeper.rect.left <= shopkeeper.ground_rect.left + 30:
            shopkeeper.rect.left = shopkeeper.ground_rect.left + 100
            shopkeeper.horizontal_velocity = 1  # Change direction to right

        # Fish logic
        fish.update()

        # Player logic
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

        # Handle hiding
        handle_hiding()

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

        # for wall in Walls:
        #     if player.rect.colliderect(wall.rect):
        #         overlap_left = wall.rect.right - player.rect.left
        #         overlap_right = player.rect.right - wall.rect.left
        #         # check if player is on the left side of the wall
        #         if abs(overlap_left) < abs(overlap_right):
        #             player.rect.left = wall.rect.right
        #         # check if player is on the right side of the wall
        #         else:
        #             player.rect.right = wall.rect.left

                # If the player is not on any platform, apply gravity
        if not on_platform and player.rect.bottom < game_map.ground_level:
            player.is_jumping = True

        player.update(clock.get_time())

        # Update player's collision rectangle
        player.collision_rect.topleft = player.rect.topleft

        camera.follow_sprite(player)
        game_map.draw(SCREEN, camera)

        for platform in platforms:
            platform.draw(SCREEN, camera)

        # for wall in Walls:
        #     wall.draw(SCREEN, camera)

        for guard in Guards:
            guard.draw(SCREEN, camera)
        # Draw the shopkeeper
        shopkeeper.draw(SCREEN, camera)

        for spot in hiding_spot_objects:
            spot.draw(SCREEN, camera, player.is_hidden and spot ==
                      current_hiding_spot)

        BUFFER = 120  # You can adjust this value based on how much space you want to allow

        # Create extended collision rectangles with the buffer
        player_buffered_rect = player.collision_rect.inflate(BUFFER, BUFFER)

        # Check if the player picks up the fish
        if not fish_picked_up:
            if player_buffered_rect.colliderect(fish.rect):
                if keys[pygame.K_q]:  # Press 'Q' to pick up the fish
                    fish_picked_up = True

        # Draw the fish in the middle of the shopkeeper's range and slightly above the ground
        if not fish_picked_up:
            fish_x = shopkeeper.ground_rect.left + \
                (shopkeeper.ground_rect.width // 2) - (fish.rect.width // 2)
            fish_y = shopkeeper.ground_rect.bottom - fish.rect.height - \
                20  # Adjust to be slightly above the ground
            fish.draw(SCREEN, fish_x - camera.x_offset, fish_y)
            fish.rect.topleft = (fish_x, fish_y)
        else:
            # Draw the fish on top of the player, touching but not covering the player
            # Ensure the fish is exactly on top of the player
            fish.rect.midbottom = player.rect.midtop
            # No gap, fish sits directly on top
            fish.rect.y = player.rect.top - fish.rect.height
            fish.rect.x = player.rect.centerx - fish.rect.width // 2  # Center horizontally
            fish.draw(SCREEN, fish.rect.x - camera.x_offset, fish.rect.y)

        player.draw(SCREEN, camera)

        for heart, heart_rect in health_display:
            SCREEN.blit(heart, heart_rect)

        pygame.display.flip()
        clock.tick(60)
