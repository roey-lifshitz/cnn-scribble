from typing import Optional, Tuple, Dict
from UI.base import UI
import pygame


class TextBox(UI):
    """
    Static input box
    """
    def __init__(self, rect,
                 color: Tuple[int, int, int] = (255, 255, 255),
                 **kwargs: Optional[Dict]) -> None:

        super().__init__(rect, kwargs)

        self.color = color
        self.font = pygame.font.SysFont(self.font, self.font_size)

        self.text = "undefined"

    def draw(self, screen, dt):
        """
        Draws input box, text and focus bar
        :param screen:
        :return:
        """
        super().draw(screen, self.color)

        # render text
        data = self.font.render(self.text, True, self.text_color)
        data_rect = data.get_rect()
        data_rect.center = self.rect.center

        screen.blit(data, data_rect)


    def handle_event(self, event: pygame.event) -> None:
        """
        Updates the input box every frame
        :param event: current user event
        :return: None
        """
        pass
