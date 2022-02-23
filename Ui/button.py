from typing import Tuple, Callable
import pygame

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
                 color: Tuple[int, int, int] = (235, 232, 232),  # Gary
                 hover_color: Tuple[int, int, int] = (196, 191, 191),  # Dark Gray
                 text_color: Tuple[int, int, int] = (0, 0, 0),
                 border_color: Tuple[int, int, int] = (0, 0, 0),
                 border_width: int = 2,
                 on_click: Callable = lambda: print("No command activated for this button")) -> None:

        self.on_click = on_click
        self.color = color

        self.hover_color = hover_color
        self.border_color = border_color
        self.border_width = border_width

        # if mouse is hovering
        self._hover = False

        # Get the rect of the button
        self.x, self.y, self.width, self.height = rect
        self.rect = pygame.Rect(rect)

        # Button contains an image
        if image:
            self.data = image
        # Button contains a text
        elif text:
            font = pygame.font.SysFont(font, font_size)
            self.data = font.render(text, True, text_color)
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
        if not self._hover:
            pygame.draw.rect(screen, self.color, self.rect)
        else:
            pygame.draw.rect(screen, self.hover_color, self.rect)

        pygame.draw.line(screen, self.border_color,
                         (self.x - self.border_width, self.y - self.border_width),
                         (self.x - self.border_width, self.y + self.height + self.border_width),
                         self.border_width)

        pygame.draw.line(screen, self.border_color,
                         (self.x + self.width, self.y - self.border_width),
                         (self.x + self.width, self.y + self.height + self.border_width),
                         self.border_width)

        # Horizontal Border Lines
        pygame.draw.line(screen, self.border_color,
                         (self.x - self.border_width, self.y - self.border_width),
                         (self.x + self.width + self.border_width, self.y - self.border_width),
                         self.border_width)

        pygame.draw.line(screen, self.border_color,
                         (self.x - self.border_width, self.y + self.height),
                         (self.x + self.width - self.border_width, self.y + self.height),
                         self.border_width)

        # Draw image/text (inside button)
        screen.blit(self.data, self.data_rect)

    def update(self, event: pygame.event) -> None:
        """
        Updates the button every frame
        :param event: current user event
        :return: None
        """

        if self.rect.collidepoint(*pygame.mouse.get_pos()):
            self._hover = True
        else:
            self._hover = False

        if self._hover:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(*pygame.mouse.get_pos()):
                    self.on_click()


