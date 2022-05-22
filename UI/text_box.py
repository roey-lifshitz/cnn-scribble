from typing import Optional, Tuple, Dict
from UI.base import UI
import pygame


class TextBox(UI):
    """
    Static input box
    """
    def __init__(self, rect,
                 text: str = None,
                 align_left: bool = False,
                 color: Tuple[int, int, int] = (255, 255, 255),
                 **kwargs: Optional[Dict]) -> None:

        super().__init__(rect, kwargs)

        self.color = color
        self.font = pygame.font.SysFont(self.font, self.font_size)

        self.align_left = align_left

        self.text = " "
        if text:
            self.text = text

    def draw(self, screen, dt):
        """
        Draws text box
        :param screen:
        :return:
        """
        super().draw(screen, self.color)

        # render text
        data = self.font.render(self.text, True, self.text_color)
        data_rect = data.get_rect()
        data_rect.center = self.rect.center

        if self.align_left:
            data_rect.left = self.rect.left

        screen.blit(data, data_rect)


    def handle_event(self, event: pygame.event) -> None:
        """
        Updates the input box every frame
        :param event: current user event
        :return: None
        """
        pass

