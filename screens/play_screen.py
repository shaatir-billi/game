import pygame
import sys
from camera import Camera
from utils.globals import *
from shopkeeper import Shopkeeper
from fish import Fish
from screens.game_over_screen import game_over
from screens.game_map import *
from screens.player import create_player, handle_player_logic
from logic.game_logic import handle_guard_collision, handle_hiding, handle_shopkeeper_collision, handle_fish_pickup
from screens.game_finish_screen import game_finish  # Import the game finish screen
# Import health display functions
from utils.health_display import create_health_display, update_health_display
# Import shopkeeper logic functions
from logic.shopkeeper_logic import handle_shopkeeper_movement, handle_shopkeeper_chase
from logic.draw_logic import draw_game_elements  # Corrected import statement


def play(SCREEN):
    game_map = create_game_map()
    camera = Camera((SCREEN_WIDTH, SCREEN_HEIGHT), map_width)

    player = create_player(game_map)

    ground = game_map.ground_level

    # Create platforms, walls, guards, and hiding spots
    platforms = create_platforms(ground)
    Walls = create_walls()
    Guards = create_guards(platforms)
    hiding_spot_objects = create_hiding_spots(platforms)

    # Add the shopkeeper on the opposite side of the wall
    shopkeeper = Shopkeeper(
        sprite_sheet_path="assets/sprites/shopkeeper/man_walk.png",
        frame_width=48,
        frame_height=48,
        scale=3,
        ground_level=ground
    )
    shopkeeper.rect.topleft = (
        Walls[0].rect.right + 200, ground - shopkeeper.rect.height)

    original_shopkeeper_position = (shopkeeper.rect.x, shopkeeper.rect.y)

    # Add the fish
    fish = Fish(
        sprite_sheet_path="assets/sprites/fish/fish.png",
        frame_width=260,
        frame_height=110,
        scale=0.5  # Adjust scale to make fish smaller
    )

    original_fish_position = (shopkeeper.rect.left + (shopkeeper.rect.width // 2) - (fish.rect.width // 2) + 450,
                              ground - fish.rect.height - 20)

    fish_picked_up = False
    # Track the fish's position when dropped
    fish_position = original_fish_position
    fish_cooldown = 500  # Cooldown period in milliseconds
    last_fish_action_time = 0

    clock = pygame.time.Clock()

    # Add persistent horizontal velocity
    player.horizontal_velocity = 0

    health_display = create_health_display(player.health)

    hiding_cooldown = 0  # Cooldown period in milliseconds
    hiding_buffer = 500  # Buffer period in milliseconds
    last_hiding_time = 0
    current_hiding_spot = None  # Track the current hiding spot

    font = pygame.font.Font(None, 24)  # Font for the message
    message_surface = font.render(
        "Fish picked up", True, (255, 255, 255))  # Rendered message surface

    barrel_image = pygame.image.load(
        "assets/map/Fishbarrel2.png").convert_alpha()
    barrel_image = pygame.transform.scale(barrel_image, (barrel_image.get_width(
    ) * 3.5, barrel_image.get_height() * 4))  # Scale the barrel image
    barrel_rect = barrel_image.get_rect(
        topleft=(0, ground - 640 - barrel_image.get_height()))

    shopkeeper_chasing = False  # Flag to indicate if the shopkeeper is chasing the player

    graph = create_graph(platforms, ground, Walls)

    while True:
        SCREEN.fill("black")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Check if 'q' key is pressed
                    print("Button pressed")
                    print("Player position:", player.rect.topleft)
                    print("Player collision rectangle:",
                          player.collision_rect.topleft)

                    fish_picked_up, fish_position, last_fish_action_time = handle_fish_pickup(
                        player, fish, fish_picked_up, fish_position, last_fish_action_time, fish_cooldown)
                if event.key == pygame.K_y:
                    # start chasing the player
                    shopkeeper_chasing = True
                    fish_picked_up = True

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
                handle_guard_collision(player, Guards, lambda: update_health_display(
                    health_display, player.health))

        # Handle guard collision
        handle_guard_collision(player, Guards, lambda: update_health_display(
            health_display, player.health))

        # Check if the player picks up the fish
        if not shopkeeper_chasing and fish_picked_up:
            shopkeeper_chasing = True  # Start chasing the player

        # Shopkeeper logic
        shopkeeper.update()
        handle_shopkeeper_movement(
            shopkeeper, player, shopkeeper_chasing, map_width, keys, graph, current_hiding_spot)
        shopkeeper_chasing = handle_shopkeeper_chase(
            shopkeeper, player, fish_picked_up, shopkeeper_chasing)

        # Handle shopkeeper collision with platforms
        # on_platform = False
        # for platform in platforms:
        #     if (
        #         shopkeeper.rect.colliderect(platform.rect)
        #         and shopkeeper.y_velocity >= 0
        #         and shopkeeper.rect.bottom <= platform.rect.top + 20
        #         and platform.rect.left <= shopkeeper.rect.centerx <= platform.rect.right
        #     ):
        #         shopkeeper.rect.bottom = platform.rect.top
        #         shopkeeper.is_jumping = False
        #         shopkeeper.y_velocity = 0
        #         on_platform = True
        #         break

        # if not on_platform and shopkeeper.rect.bottom < game_map.ground_level:
        #     shopkeeper.is_jumping = True

        # # Handle shopkeeper collision with walls
        # for wall in Walls:
        #     if shopkeeper.rect.colliderect(wall.rect):
        #         overlap_left = wall.rect.right - shopkeeper.rect.left
        #         overlap_right = shopkeeper.rect.right - wall.rect.left
        #         if abs(overlap_left) < abs(overlap_right):
        #             shopkeeper.rect.left = wall.rect.right
        #         else:
        #             shopkeeper.rect.right = wall.rect.left

        # Handle shopkeeper collision
        fish_picked_up, fish_position = handle_shopkeeper_collision(
            player, shopkeeper, fish_picked_up, original_shopkeeper_position, original_fish_position)

        # Fish logic
        fish.update()

        # Player logic
        handle_player_logic(player, keys)

        # Handle hiding
        last_hiding_time, current_hiding_spot = handle_hiding(
            player, hiding_spot_objects, keys, last_hiding_time, hiding_cooldown, hiding_buffer, current_hiding_spot)

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

        player.update(clock.get_time())

        # Update player's collision rectangle
        player.collision_rect.topleft = player.rect.topleft

        camera.follow_sprite(player)
        game_map.draw(SCREEN, camera)

        draw_game_elements(SCREEN, camera, game_map, platforms, Guards, shopkeeper, hiding_spot_objects, fish, fish_picked_up,
                           fish_position, player, message_surface, barrel_image, barrel_rect, health_display, current_hiding_spot, Walls)

        if ENABLE_GRAPH_VISUALIZATION:
            graph.draw(SCREEN, camera)
        # Check if the player reaches the barrel with the fish
        if fish_picked_up and player.collision_rect.colliderect(barrel_rect):
            game_finish(SCREEN)  # Display the game finish screen
            return  # Exit the play function to stop the game loop

        pygame.display.flip()
        clock.tick(60)
