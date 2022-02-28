from typing import Tuple, Callable
from datetime import time
import warnings
import pygame

class Timer:

    def __init__(self,
                 rect: Tuple[int, int, int, int],
                 start_time: str,
                 color: Tuple[int, int, int] = (255, 255, 255),
                 font: str = "Ariel",
                 font_size: int = 30,
                 text_color: Tuple[int, int, int] = (0, 0, 0),
                 border_color: Tuple[int, int, int] = (0, 0, 0),
                 border_width: int = 2) -> None:# needs to be 'hh:mm:ss' format


        # Parse the clock string into a list
        self.start_time = list(t[:-1] for t in start_time.split(':'))
        self.clock = self.start_time

        self.total_time = 0

        self.color = color
        self.font = pygame.font.SysFont(font, font_size)
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width

        self._finish = False


        # Get the rect of the Timer
        self.x, self.y, self.width, self.height = rect
        self.rect = pygame.Rect(rect)

    def restart(self):
        self._finish = False
        self.clock = self.start_time

    def _tick(self):

        # find total amount of seconds
        total_seconds = int(self.clock[0]) * 60 * 60 + int(self.clock[1]) * 60 + int(self.clock[2])
        if total_seconds > 0:
            total_seconds -= 1;
            h, remaining_seconds = divmod(total_seconds, 60 * 60)
            m, s = divmod(remaining_seconds, 60)

            self.clock[0] = '0' + str(h) if h < 10 else str(h)
            self.clock[1] = '0' + str(m) if m < 10 else str(m)
            self.clock[2] = '0' + str(s) if s < 10 else str(s)
        else:
            self._finish = True
            self.clock = self.start_time



    def draw(self, screen: pygame.display, dt):
        """
        Draw 4 lines (Borders) around the button and then fills them with color
        :param screen: display of game
        :return: None
        """
        # Draw main box
        pygame.draw.rect(screen, self.color, self.rect)

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

        self.total_time += dt
        if not self._finish:
            if self.total_time > 1000:
                self._tick()
                self.total_time = 0

        text = ''
        flag = True
        for i in range(len(self.clock)):
            if (self.clock[i] == '00' or self.clock[i] == 0) and flag:
                continue
            else:
                flag = False
            text += self.clock[i] + ':'

        data = self.font.render(text[:-1], True, self.text_color)
        data_rect = data.get_rect()
        data_rect.center = self.rect.center

        # Draw Numbers
        screen.blit(data, data_rect)

    def update(self):
        pass