import pygame
import sys
from enemy import Enemy
from sprite import Sprite
from map import GameMap
from camera import Camera
from utils.globals import SCREEN_WIDTH, SCREEN_HEIGHT
from utils.globals import *

def play(SCREEN):
    game_map = GameMap("assets/map/sky.jpeg")
    camera = Camera((SCREEN_WIDTH, SCREEN_HEIGHT), map_width)

    # Player (cat sprite)
    player = Sprite(
        sprite_sheet_path="assets/sprites/player/sprite_sheet.png",
        x=100,
        y=SCREEN_HEIGHT - 150,  # This places the cat at the ground level
        frame_width=32,
        frame_height=32,
        scale=5
    )

    # Enemy (an example with a walking animation)
    enemy = Enemy(
        sprite_sheet_path="assets/sprites/enemy/hehe.png",  # Path to your enemy sprite sheet
        x=500,  # Adjust the x-coordinate for enemy placement
        y=SCREEN_HEIGHT - 150,  # Align it with the ground level like the player
        frame_width=30,
        frame_height=59,
        scale=5  # Same scale factor
    )

    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60) / 1000  # Delta time in seconds
        SCREEN.fill("black")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_a]:
            dx = -5
            player.set_animation(5)
        if keys[pygame.K_d]:
            dx = 5
            player.set_animation(5)
        if keys[pygame.K_w]:
            player.jump()

        player.move(dx, dy)
        player.update()

        # Update enemy
        enemy.update(dt)  # Pass delta time to control animation/movement

        # Check for collision between player and enemy
        if player.rect.colliderect(enemy.rect):
            # If collision occurs, game over
            game_over(SCREEN)
            return  # Exit the game loop

        # Update camera to follow player
        camera.follow_sprite(player)

        # Draw map, player, and enemy
        game_map.draw(SCREEN, camera)
        player.draw(SCREEN, camera)
        enemy.draw(SCREEN, camera)  # Draw the enemy

        pygame.display.flip()

# Game over function to handle what happens when the player collides with the enemy
def game_over(SCREEN):
    font = pygame.font.SysFont("Arial", 50)
    game_over_text = font.render("Game Over", True, (255, 0, 0))  # Red text
    SCREEN.fill((0, 0, 0))  # Fill screen with black
    SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    
    # Wait for a moment before closing
    pygame.time.wait(2000)  # Wait for 2 seconds
    pygame.quit()
    sys.exit()
