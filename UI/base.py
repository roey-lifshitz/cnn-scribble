from typing import Optional, Tuple, Dict
from abc import ABC, abstractmethod

import warnings
import pygame

""" Default kwargs for all Ui elements (although some don't use them) """
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
    """ Base class for a UI element """

    def __init__(self,
                 rect: Tuple[int, int, int, int],
                 params: Optional[Dict] = None) -> None:

        # Variables for UI elements
        self.x, self.y, self.width, self.height = rect
        self.rect = pygame.Rect(rect)

        # add default values for key worded arguments
        self.__dict__.update(default_kwargs)

        # update values for given key worded arguments
        for key, val in params.items():
            if key in default_kwargs:
                self.__dict__.update({key: val})
            else:
                warnings.warn(f'{key} not recognized')

    @abstractmethod
    def handle_event(self, event: pygame.event) -> None:
        """
        Handles events of the UI element
        Should be called for every event in the game inside the game main loop
        :param event: pygame even
        :return: None
        """
        pass

    def draw(self, screen: pygame.Surface, color: Tuple[int, int, int]) -> None:
        """
        Draws the basics of the UI element-
         background and the borders
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


