import pygame
import sys


def game_finish(SCREEN):
    from screens.main_menu import main_menu  # Import the main menu screen
    from screens.play_screen import play  # Import the play screen

    font = pygame.font.Font(None, 36)
    message_surface = font.render("Game Finished!", True, (255, 255, 255))
    message_rect = message_surface.get_rect(
        center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2 - 50))

    play_again_surface = font.render("Play Again", True, (255, 255, 255))
    play_again_rect = play_again_surface.get_rect(
        center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2 + 10))

    main_menu_surface = font.render("Main Menu", True, (255, 255, 255))
    main_menu_rect = main_menu_surface.get_rect(
        center=(SCREEN.get_width() // 2, SCREEN.get_height() // 2 + 50))

    while True:
        SCREEN.fill("black")
        SCREEN.blit(message_surface, message_rect)
        SCREEN.blit(play_again_surface, play_again_rect)
        SCREEN.blit(main_menu_surface, main_menu_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(event.pos):
                    play(SCREEN)  # Start a new game
                elif main_menu_rect.collidepoint(event.pos):
                    main_menu(SCREEN)  # Go to the main menu

        pygame.display.flip()
