import pygame
from sprite import Sprite


def create_player(game_map):
    player = Sprite(
        sprite_sheet_path="assets/sprites/player/sprite_sheet.png",
        x=100,
        y=game_map.ground_level - 150,  # Adjust to spawn above the ground
        frame_width=32,
        frame_height=32,
        scale=5,
        ground_level=game_map.ground_level  # Pass ground level to the sprite
    )
    return player


def handle_player_logic(player, keys):
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
