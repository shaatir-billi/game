import pygame


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/fonts/main.ttf", size)


def draw_text_with_border(screen, text, font, text_color, border_color, pos, border_width=2):
    """
    Draws text with a border.
    :param screen: The surface to draw the text on.
    :param text: The text to be displayed.
    :param font: The font object.
    :param text_color: Color of the text.
    :param border_color: Color of the border.
    :param pos: Position to draw the text (x, y).
    :param border_width: Width of the border.
    """
    # Create the text surface
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=pos)

    # Draw the border by rendering the text several times with offsets
    for x_offset in range(-border_width, border_width + 1):
        for y_offset in range(-border_width, border_width + 1):
            if x_offset != 0 or y_offset != 0:  # Skip the center text
                # Render the border text with the border color
                border_surface = font.render(text, True, border_color)
                border_rect = border_surface.get_rect(
                    center=(text_rect.centerx + x_offset, text_rect.centery + y_offset))
                screen.blit(border_surface, border_rect)

    # Draw the main text over the border
    screen.blit(text_surface, text_rect)
