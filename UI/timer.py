from typing import Optional, Tuple, Dict, Callable
from UI.base import UI
import pygame
import warnings
import pygame

class Timer(UI):

    def __init__(self,
                 rect: Tuple[int, int, int, int],
                 start_time: str,
                 color: Tuple[int, int, int] = (255, 255, 255),
                 **kwargs: Optional[Dict]) -> None:

        super().__init__(rect, kwargs)
        # Parse the clock string into a list
        self.start_time = list(t[:-1] for t in start_time.split(':'))
        self.clock = self.start_time

        self.total_time = 0

        self.color = color
        self.font = pygame.font.SysFont(self.font, self.font_size)

        self.finish = False


    def restart(self):
        self.finish = False
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
            self.finish = True
            self.clock = self.start_time

    def draw(self, screen: pygame.display, dt):
        """
        Draw 4 lines (Borders) around the button and then fills them with color
        :param screen: display of game
        :return: None
        """

        super().draw(screen, self.color)

        self.total_time += dt
        if not self.finish:
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

    def handle_event(self, event: pygame.event) -> bool:

        return self.finish
