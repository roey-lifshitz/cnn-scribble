from abc import ABC, abstractmethod
from typing import Optional, Tuple, Dict

import warnings
import pygame

default_kwargs = \
    {
        'has_border': True,
        'border_width': 2,
        'border_color': (0, 0, 0),
        'font': 'Ariel',
        'font_size': 30,
        'text_color': (0, 0, 0)
    }


class UI(ABC):

    def __init__(self,
                 rect: Tuple[int, int, int, int],
                 params: Optional[Dict] = None) -> None:

        self.x, self.y, self.width, self.height = rect
        self.rect = pygame.Rect(rect)

        # default values for key worded arguments
        self.__dict__.update(default_kwargs)

        # update values for given key worded arguments
        for key, val in params.items():
            if key in default_kwargs:
                self.__dict__.update({key: val})
            else:
                warnings.warn(f'{key} not recognized')

    @abstractmethod
    def handle_event(self, event: pygame.event) -> None:
        pass


    def draw(self, screen: pygame.Surface, color: Tuple[int, int, int]) -> None:
        """
        Draws backgrounf and the borders of a ui element
        :param screen: pygame display
        :param color r, g, b of color to fill borders with
        :return: None
        """

        # Draw Bigger rect to create the illusion of a border
        if self.has_border:
            pygame.draw.rect(screen, self.border_color, (self.x - self.border_width,
                                                         self.y - self.border_width,
                                                         self.width + self.border_width * 2,
                                                         self.height + self.border_width * 2))

        pygame.draw.rect(screen, color, self.rect)


