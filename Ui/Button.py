from typing import Tuple, Callable
import pygame
GRAY = (235, 232, 232)
HOVER_GRAY = (196, 191, 191)
BLACK = (0, 0, 0)


class Button:
    """
        This class represents an editable button that can be added onto a pygame screen
        Draws either a string or an image on top of the button
        Must receive either a image or test param
    """
    def __init__(self,
                 rect: Tuple[int, int, int, int],
                 text: str = None,
                 font: str = "Ariel",
                 font_size: int = 30,
                 image: pygame.Surface = None,
                 color: Tuple[int, int, int] = GRAY,
                 hover_color: Tuple[int, int, int] = HOVER_GRAY,
                 border_color: Tuple[int, int, int] = BLACK,
                 border_width: int = 2,
                 on_click: Callable = lambda: print("No command activated for this button")) -> None:

        self.on_click = on_click
        self.color = color

        self.hover_color = hover_color
        self.border_color = border_color
        self.border_width = border_width

        # if mouse is hovering
        self.hover = False

        # Get the rect of the button
        self.x, self.y, self.w, self.h = rect
        self.rect = pygame.Rect(rect)

        # Button contains an image
        if image:
            self.data = image
        # Button contains a text
        elif text:
            font = pygame.font.SysFont(font, font_size)
            self.data = font.render(text, True, BLACK)
        else:
            raise Exception('Not specified if text or image!')

        self.data_rect = self.data.get_rect()

        # Center the image/text in relation to the button
        self.data_rect.center = self.rect.center

    def draw(self, screen: pygame.display):
        """
        Draw 4 lines (Borders) around the button and then fills them with color
        :param screen: display of game
        :return: None
        """
        # Rect between lines
        if not self.hover:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
        else:
            pygame.draw.rect(screen, self.hover_color, (self.x, self.y, self.w, self.h))

        # Vertical Border Lines
        pygame.draw.line(screen, self.border_color, (self.x, self.y), (self.x, self.y + self.h),
                         self.border_width)
        pygame.draw.line(screen, self.border_color, (self.x + self.w, self.y), (self.x + self.w, self.y + self.h),
                         self.border_width)
        # Horizontal Border Lines
        pygame.draw.line(screen, self.border_color, (self.x, self.y), (self.x + self.w, self.y),
                         self.border_width)
        pygame.draw.line(screen, self.border_color, (self.x, self.y + self.h), (self.x + self.w, self.y + self.h),
                         self.border_width)

        # Draw image/text (inside button)
        screen.blit(self.data, self.data_rect)

    def is_click(self, mouse_pos):
        """
        Check if mouse hovering on top of button
        """
        if self.rect.collidepoint(*mouse_pos):
            self.hover = True
            return True
        self.hover = False
        return False

    def click(self):
        """
            Check if mouse clicking buton
        """
        if self.hover:
            print(self.hover)
            self.hover = False
            self.on_click()
            return True
        return False



