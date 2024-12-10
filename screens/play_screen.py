import pygame
import sys
from sprite import Sprite
from map import GameMap
from camera import Camera
from utils.globals import SCREEN_WIDTH, SCREEN_HEIGHT
from utils.globals import *


def play(SCREEN):
    game_map = GameMap("assets/map/sky.jpeg")
    camera = Camera((SCREEN_WIDTH, SCREEN_HEIGHT), map_width)

    player = Sprite(
        sprite_sheet_path="assets/sprites/player/sprite_sheet.png",
        x=100,
        y=SCREEN_HEIGHT - 150,  # This should place the cat at the ground level
        frame_width=32,
        frame_height=32,
        scale=5
    )

    clock = pygame.time.Clock()

    while True:
        SCREEN.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_a]:
            dx = -5
            player.set_animation(5)
        if keys[pygame.K_d]:
            dx = 5
            player.set_animation(5)

        # Jumping now triggered by the W key
        if keys[pygame.K_w]:
            player.jump()

        player.move(dx, dy)
        player.update()

        camera.follow_sprite(player)
        game_map.draw(SCREEN, camera)
        player.draw(SCREEN, camera)

        pygame.display.flip()
        clock.tick(60)
