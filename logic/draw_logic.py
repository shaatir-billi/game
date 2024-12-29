import pygame


def draw_game_elements(SCREEN, camera, game_map, platforms, Guards, shopkeeper, hiding_spot_objects, fish, fish_picked_up, fish_position, player, message_surface, barrel_image, barrel_rect, health_display, current_hiding_spot, Walls, player_health):
    for platform in platforms:
        platform.draw(SCREEN, camera)

    for guard in Guards:
        guard.draw(SCREEN, camera)

    shopkeeper.draw(SCREEN, camera)

    for wall in Walls:
        wall.draw(SCREEN, camera)

    for spot in hiding_spot_objects:
        spot.draw(SCREEN, camera, player.is_hidden and spot ==
                  current_hiding_spot)

    if not fish_picked_up:
        fish.draw(SCREEN, fish_position[0] - camera.x_offset, fish_position[1])
        fish.rect.topleft = fish_position
    else:
        message_rect = message_surface.get_rect(
            center=(player.rect.centerx - camera.x_offset, player.rect.bottom + 5))
        SCREEN.blit(message_surface, message_rect)

    player.draw(SCREEN, camera)

    for heart, heart_rect in health_display:
        SCREEN.blit(heart, heart_rect)

    font = pygame.font.Font("assets/fonts/main.ttf", 20)
    lives_text = font.render(
        f"{player_health} lives left", True, (0, 0, 0))
    lives_rect = lives_text.get_rect(topleft=(20, 60))
    SCREEN.blit(lives_text, lives_rect)

    SCREEN.blit(barrel_image, (barrel_rect.x - camera.x_offset, barrel_rect.y))
