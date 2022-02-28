from abc import ABC, abstractmethod
from typing import Optional, Tuple, Dict

import warnings
import pygame
default_kwargs = {'has_border': True, 'border_width': 2, 'border_color': (0, 0, 0)}

class Ui(ABC):

    def __init__(self,
                 rect: Tuple[int, int, int, int],
                 bg_color: Tuple[int, int, int, int],
                 **kwargs: Optional[Dict]) -> None:

        self.x, self.y, self.width, self.height = rect
        self.rect = pygame.Rect(rect)
        self.bg_color = bg_color

        self._focused = False

        # default values for key worded arguments
        self.__dict__.update(default_kwargs)

        # update values for given key worded arguments
        for key, val in kwargs.items():
            if key in default_kwargs:
                self.__dict__.update({key:val})
            else:
                warnings.warn(f'{key} not recognized')


    def draw(self, screen: pygame.Surface) -> None:

        screen.blit(self.bg_color, self.rect)

        # Draw Border
        if self.has_border:
            # Horizontal Border Lines
            pygame.draw.line(screen, self.border_color,
                             (self.x - self.border_width, self.y - self.border_width),
                             (self.x - self.border_width, self.y + self.height + self.border_width),
                             self.border_width)

            pygame.draw.line(screen, self.border_color,
                             (self.x + self.width, self.y - self.border_width),
                             (self.x + self.width, self.y + self.height + self.border_width),
                             self.border_width)

            # Vertical Border Lines
            pygame.draw.line(screen, self.border_color,
                             (self.x - self.border_width, self.y - self.border_width),
                             (self.x + self.width + self.border_width, self.y - self.border_width),
                             self.border_width)

            pygame.draw.line(screen, self.border_color,
                             (self.x - self.border_width, self.y + self.height),
                             (self.x + self.width - self.border_width, self.y + self.height),
                             self.border_width)

    @abstractmethod
    def handle_event(self, event: pygame.event) -> None:
        pass



