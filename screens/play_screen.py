import pygame
import sys
from sprite import Sprite
from map import *
from camera import Camera
from utils.globals import *
from shopkeeper import Shopkeeper
from fish import Fish
from screens.setup_map import create_platforms, create_walls, create_guards, create_hiding_spots
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

    # Create platforms, walls, guards, and hiding spots
    platforms = create_platforms(ground)
    Walls = create_walls()
    Guards = create_guards(platforms)
    hiding_spot_objects = create_hiding_spots(platforms)

    # Add the shopkeeper on the opposite side of the wall
    shopkeeper = Shopkeeper(
        sprite_sheet_path="assets/sprites/shopkeeper/man_walk.png",
        ground_rect=pygame.Rect(
            Walls[0].rect.right + 200, Walls[0].rect.top, 600, Walls[0].rect.height),
        frame_width=48,
        frame_height=48,
        scale=3
    )

    original_shopkeeper_position = (shopkeeper.rect.x, shopkeeper.rect.y)

    # Add the fish
    fish = Fish(
        sprite_sheet_path="assets/sprites/fish/fish.png",
        frame_width=260,
        frame_height=110,
        scale=0.5  # Adjust scale to make fish smaller
    )

    original_fish_position = (shopkeeper.ground_rect.left + (shopkeeper.ground_rect.width // 2) - (fish.rect.width // 2),
                              shopkeeper.ground_rect.bottom - fish.rect.height - 20)

    fish_picked_up = False
    # Track the fish's position when dropped
    fish_position = original_fish_position
    fish_cooldown = 500  # Cooldown period in milliseconds
    last_fish_action_time = 0

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

    font = pygame.font.Font(None, 24)  # Font for the message
    message_surface = font.render(
        "Fish picked up", True, (255, 255, 255))  # Rendered message surface

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

    def handle_shopkeeper_collision():
        nonlocal fish_picked_up, fish_position
        if fish_picked_up and player.collision_rect.colliderect(shopkeeper.collision_rect):
            fish_picked_up = False
            # Reset positions of shopkeeper and fish
            shopkeeper.rect.topleft = original_shopkeeper_position
            fish_position = original_fish_position

    while True:
        SCREEN.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                current_time = pygame.time.get_ticks()
                if event.key == pygame.K_q and current_time - last_fish_action_time > fish_cooldown:
                    if not fish_picked_up and player.collision_rect.colliderect(fish.rect):
                        fish_picked_up = True
                        print("Fish picked up")
                    elif fish_picked_up:
                        fish_picked_up = False
                        # Drop the fish at the player's position
                        fish_position = (player.rect.centerx,
                                         player.rect.bottom - fish.rect.height // 2)
                        print("Fish dropped")
                    last_fish_action_time = current_time

        keys = pygame.key.get_pressed()

        # Guards logic
        for guard in Guards:
            guard.update()
            guard.move(guard.horizontal_velocity, 0)  # Move guard

            # Change direction slightly before reaching the platform's edge
            if guard.rect.right >= guard.platform_rect.right - 30:
                guard.rect.right = guard.platform_rect.right - 100
                guard.horizontal_velocity = -1  # Change direction to left
            elif guard.rect.left <= guard.platform_rect.left + 30:
                guard.rect.left = guard.platform_rect.left + 100
                guard.horizontal_velocity = 1  # Change direction to right

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

        # Handle shopkeeper collision
        handle_shopkeeper_collision()

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

        # Draw the fish in the middle of the shopkeeper's range and slightly above the ground
        if not fish_picked_up:
            fish.draw(SCREEN, fish_position[0] -
                      camera.x_offset, fish_position[1])
            fish.rect.topleft = fish_position
        else:
            # Draw the "Fish picked up" message above the player
            message_rect = message_surface.get_rect(
                center=(player.rect.centerx - camera.x_offset, player.rect.top - 10))
            SCREEN.blit(message_surface, message_rect)

        player.draw(SCREEN, camera)

        for heart, heart_rect in health_display:
            SCREEN.blit(heart, heart_rect)

        pygame.display.flip()
        clock.tick(60)
