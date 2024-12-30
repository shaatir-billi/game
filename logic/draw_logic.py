import pygame
from utils.globals import *


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

    # draw inanimate objects

    right_pointer = pygame.image.load(
        'assets/map/pointers/1.png').convert_alpha()
    # scale the image
    right_pointer = pygame.transform.scale(right_pointer, (40, 50))

    right_up_pointer = pygame.image.load(
        'assets/map/pointers/3.png').convert_alpha()
    right_up_pointer = pygame.transform.scale(right_up_pointer, (40, 50))

    left_up_pointer = pygame.image.load(
        'assets/map/pointers/4.png').convert_alpha()
    left_up_pointer = pygame.transform.scale(left_up_pointer, (40, 50))

    left_pointer = pygame.image.load(
        'assets/map/pointers/2.png').convert_alpha()
    left_pointer = pygame.transform.scale(left_pointer, (40, 50))

    right_pointers = [
        right_pointer.get_rect(topleft=(200, SCREEN_HEIGHT - 80)),
        right_pointer.get_rect(topleft=(1400, SCREEN_HEIGHT - 80)),
        right_pointer.get_rect(topleft=(2850, 100)),
    ]

    right_up_pointers = [
        right_up_pointer.get_rect(topleft=(1800, SCREEN_HEIGHT - 80)),
        right_up_pointer.get_rect(topleft=(2050, 170)),
        right_up_pointer.get_rect(topleft=(1450, 250)),
    ]

    left_up_pointers = [
        left_up_pointer.get_rect(topleft=(2200, 660)),
        left_up_pointer.get_rect(topleft=(1000, 250)),
    ]

    left_pointers = [
        left_pointer.get_rect(topleft=(1750, 530)),
        left_pointer.get_rect(topleft=(2810, 100)),
    ]

    for pointer in right_pointers:
        SCREEN.blit(right_pointer, (pointer.x - camera.x_offset, pointer.y))

    for pointer in right_up_pointers:
        SCREEN.blit(right_up_pointer, (pointer.x - camera.x_offset, pointer.y))

    for pointer in left_up_pointers:
        SCREEN.blit(left_up_pointer, (pointer.x - camera.x_offset, pointer.y))

    for pointer in left_pointers:
        SCREEN.blit(left_pointer, (pointer.x - camera.x_offset, pointer.y))
