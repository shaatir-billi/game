import pygame
from screens.player import handle_player_logic


def handle_guard_collision(player, Guards, update_health_display):
    if not player.is_invincible:
        for guard in Guards:
            if player.collision_rect.colliderect(guard.collision_rect):
                # Check if the player is above the guard
                if player.rect.bottom <= guard.rect.top + 10:
                    # Player is above the guard, no damage taken
                    continue
                player.take_damage()
                update_health_display()


def handle_hiding(player, hiding_spot_objects, keys, last_hiding_time, hiding_cooldown, hiding_buffer, current_hiding_spot):
    current_time = pygame.time.get_ticks()
    if current_time - last_hiding_time > hiding_cooldown:
        for spot in hiding_spot_objects:
            if player.rect.colliderect(spot.rect):
                if keys[pygame.K_e] and current_time - last_hiding_time > hiding_buffer:
                    if player.is_hidden:
                        player.unhide()
                        current_hiding_spot = None
                    else:
                        player.hide()
                        current_hiding_spot = spot
                    last_hiding_time = current_time
    return last_hiding_time, current_hiding_spot


def handle_shopkeeper_collision(player, shopkeeper, fish_picked_up, original_shopkeeper_position, original_fish_position):
    fish_position = original_fish_position  # Ensure fish_position is assigned
    if fish_picked_up and player.collision_rect.colliderect(shopkeeper.collision_rect):
        fish_picked_up = False
        # Reset positions of shopkeeper and fish
        shopkeeper.rect.topleft = original_shopkeeper_position
        fish_position = original_fish_position
    return fish_picked_up, fish_position


def handle_fish_pickup(player, fish, fish_picked_up, fish_position, last_fish_action_time, fish_cooldown):
    current_time = pygame.time.get_ticks()
    if current_time - last_fish_action_time > fish_cooldown:
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
    return fish_picked_up, fish_position, last_fish_action_time
