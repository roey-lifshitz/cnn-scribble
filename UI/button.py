from typing import Optional, Tuple, Dict, Callable
from UI.base import UI
import pygame

class Button(UI):
    """
        This class represents an editable button that can be added onto a pygame screen
        Draws either a string or an image on top of the button
        Must receive either a image or test param
    """
    def __init__(self,
                 rect: Tuple[int, int, int, int],
                 text: str = None,
                 image: pygame.Surface = None,
                 color: Tuple[int, int, int] = (235, 232, 232),  # Gary
                 hover_color: Tuple[int, int, int] = (196, 191, 191),  # Dark Gray
                 on_click: Callable = lambda: print("No command activated for this button"),
                 **kwargs: Optional[Dict]) -> None:

        super().__init__(rect, kwargs)

        self.color = color
        self.hover_color = hover_color

        self.on_click = on_click

        # Get the rect of the button
        self.x, self.y, self.width, self.height = rect
        self.rect = pygame.Rect(rect)

        # Button contains an image
        if image:
            self.data = image
        # Button contains a text
        elif text:
            font = pygame.font.SysFont(self.font, self.font_size)
            self.data = font.render(text, True, self.text_color)
        else:
            raise Exception('Not specified if text or image!')

        self.data_rect = self.data.get_rect()
        # Center the image/text in relation to the button
        self.data_rect.center = self.rect.center

        # if mouse is hovering
        self.hover = False

    def draw(self, screen: pygame.display, dt):
        """
        Draw 4 lines (Borders) around the button and then fills them with color
        :param screen: display of game
        :return: None
        """
        # Rect between lines
        if not self.hover:
            super().draw(screen, self.color)
        else:
            super().draw(screen, self.hover_color)

        # Draw image/text (inside button)
        screen.blit(self.data, self.data_rect)

    def handle_event(self, event: pygame.event) -> None:
        """
        Updates the button every frame
        :param event: current user event
        :return: None
        """
        if self.rect.collidepoint(*pygame.mouse.get_pos()):
            self.hover = True
        else:
            self.hover = False

        if self.hover:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.on_click()


