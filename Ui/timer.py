from typing import Tuple, Callable
from datetime import time
import warnings
import pygame

class Timer:

    def __init__(self,
                 rect: Tuple[int, int, int, int],
                 start_time: str, ) -> None:# needs to be 'hh:mm:ss' format


        # Parse the clock string into a list
        self.start_time = list(t[:-1] for t in start_time.split(':'))
        self.clock = self.start_time

        # Create the numbers dictionary-> each num get an appropriate image
        self.numbers = list(pygame.image.load(f'images/numbers/n{i}.png') for i in range(10))

        self._finish = False


        # Get the rect of the Timer
        self.x, self.y, self.w, self.h = rect
        self.rect = pygame.Rect(rect)

    def restart(self):
        self._finish = False
        self.clock = self.start_time

    def _tick(self):

        if self.clock[0] > 0:
            self.clock[0] -= 1
        elif self.clock[1] > 0:
            self.clock[1] -= 1
        elif self.clock[2] > 0:
            self.clock -= 1
        else:
            self._finish = True
            # Timer ended
            print("End Timer!")

    def _create_surface(self):

        # move index forward until reaches first number that is different from zero
        hours = self.start_time[0]
        minutes = self.start_time[1]
        seconds = self.start_time[2]

        if hours == 0:
            if minutes == 0:
                if seconds == 0:
                    raise ValueError('Timer is set to zero')

                if seconds < 10:
                    surf = pygame.Surface()



        # Timers is set to 0h:0m:0s
        if i == len(self.numbers):
            warnings.warn("Timer is set to zero seconds")
            return self.numbers


    def draw(self, screen: pygame.display):
        """
        Draw 4 lines (Borders) around the button and then fills them with color
        :param screen: display of game
        :return: None
        """
        pygame.draw.line(screen, self.border_color,
                         (self.x - self.border_width, self.y - self.border_width),
                         (self.x - self.border_width, self.y + self.height + self.border_width),
                         self.border_width)

        pygame.draw.line(screen, self.border_color,
                         (self.x + self.width + self.border_width, self.y - self.border_width),
                         (self.x + self.width + self.border_width, self.y + self.height + self.border_width),
                         self.border_width)

        # Horizontal Border Lines
        pygame.draw.line(screen, self.border_color,
                         (self.x - self.border_width, self.y - self.border_width),
                         (self.x + self.width + self.border_width, self.y - self.border_width),
                         self.border_width)

        pygame.draw.line(screen, self.border_color,
                         (self.x - self.border_width, self.y + self.height + self.border_width),
                         (self.x + self.width - self.border_width, self.y + self.height + self.border_width),
                         self.border_width)

        # Draw Numbers
        screen.blit(self.data, self.data_rect)