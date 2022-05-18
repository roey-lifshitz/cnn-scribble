from typing import Optional, Tuple, Dict
from UI.base import UI
import pygame


class InputBox(UI):
    """
    Static input box
    """
    def __init__(self, rect,
                 padding: int = 10,
                 color: Tuple[int, int, int] = (255, 255, 255),
                 focus_offset: int = 9,
                 focus_interval: float = 0.95,
                 **kwargs: Optional[Dict]) -> None:

        super().__init__(rect, kwargs)

        self.padding = padding
        self.color = color
        self.focus_color = (255, 255, 255)
        self.focus_offset = focus_offset
        self.focus_interval = focus_interval
        self.font = pygame.font.SysFont(self.font, self.font_size)

        self.total_time = 0

        # for text
        self.text = ""
        self.index = 0

        # boolean when to update
        self.hover = False
        self.type = "Input"

    def _finish(self) -> None:
        """
        Called when user finished writing his input (pressed enter)
        :return:
        """
        tmp = self.text
        self.text = ""
        self.index = 0
        return tmp

    def _draw_focus(self, screen: pygame.Surface, color: Tuple[int, int, int]) -> None:
        """
        Draws the focus bar
        :param screen: screen to draw on
        :param color: r, g, b of color to give the focus bar
        :return: None
        """
        # Calculate focus location
        x = self.x + self.font.render(self.text[:self.index], True, self.text_color).get_rect().width
        # Add small offset
        x += self.focus_offset

        pygame.draw.line(screen, color, (x, self.y * 1.01), (x, self.y * 0.99 + self.height), 2)

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
        data_rect.midleft = self.rect.midleft[0] + self.padding, self.rect.midleft[1]

        if self.hover:
            self.total_time += dt

        # self.time is in milliseconds so we multiply focus interval by 1000
        if self.total_time > self.focus_interval * 1000:
            # swap color between black and white
            self.focus_color = tuple(c ^ 255 for c in self.focus_color)
            self.total_time = 0

        self._draw_focus(screen, self.focus_color)
        screen.blit(data, data_rect)


    def handle_event(self, event: pygame.event) -> Optional[str]:
        """
        Updates the input box every frame
        :param event: current user event
        :return: string of text when user presses enter
        """
        # count time for focus color switch
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(*pygame.mouse.get_pos()):
                self.hover = True

            else:
                self.hover = False
                self.focus_color = (255, 255, 255)
        # Continue writing until clicked again
        if self.hover:
            # handles text in input box
            if event.type == pygame.KEYDOWN:
                self.total_time = 0
                self.focus_color = (0, 0, 0)
                # Entered space
                if event.key == pygame.K_RETURN:
                    return self._finish()

                # Backspace- remove character
                elif event.key == pygame.K_BACKSPACE:
                    if self.index > 0:
                        self.index = max(0, self.index - 1)
                        self.text = self.text[:self.index] + self.text[self.index + 1:]

                # Keys- update index location
                elif event.key == pygame.K_LEFT:
                    self.index = max(0, self.index - 1)
                elif event.key == pygame.K_RIGHT:
                    self.index = min(len(self.text), self.index + 1)

                # Character- add to text
                else:
                    # Check if in english alphabet or space bar
                    # a-z: 97-122, A-Z: 65-90, Space= 32
                    if 97 <= event.key <= 122 or 65 <= event.key <= 90 or event.key == 32:
                        # Check if can add a new letter
                        new_width = self.font.render(self.text + event.unicode, True, self.text_color).get_rect()
                        if new_width.w < self.width - self.padding * 2:
                            self.index += 1
                            self.text = self.text[:self.index - 1] + event.unicode + self.text[self.index - 1:]
