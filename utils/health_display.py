import pygame


def create_health_display(health):
    health_display = []
    for i in range(health):
        heart = pygame.image.load(
            'assets/menu/heart_32x32.png').convert_alpha()
        heart_rect = heart.get_rect(topleft=(20 + i * 30, 20))
        health_display.append((heart, heart_rect))
    return health_display


def update_health_display(health_display, health):
    for i, (heart, heart_rect) in enumerate(health_display):
        heart_rect.topleft = (20 + i * 30, 20)
        if i < health:
            heart.set_alpha(255)
        else:
            heart.set_alpha(0)
