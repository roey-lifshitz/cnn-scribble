from typing import Tuple
import pygame

class InputBox:
    """
    Static input box
    """
    def __init__(self, rect,
                 padding: int = 10,
                 font: str = "Ariel",
                 font_size: int = 30,
                 color: Tuple[int, int, int] = (255, 255, 255),
                 text_color: Tuple[int, int, int] = (0, 0, 0),
                 border_color: Tuple[int, int, int] = (0, 0, 0),
                 border_width: int = 2,
                 focus_offset: int = 9,
                 focus_interval: float = 0.95
                 ) -> None:

        self.padding = padding
        self.color = color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.focus_color = (255, 255, 255)
        self.focus_offset = focus_offset
        self.focus_interval = focus_interval
        self.font = pygame.font.SysFont(font, font_size)

        # For focus bar
        self.clock = pygame.time.Clock()
        self.time = 0

        # for text
        self.text = ""
        self.index = 0

        # boolean when to update
        self.hover = False

        # Get the rect of the button
        self.x, self.y, self.w, self.h = rect
        self.rect = pygame.Rect(rect)


    def _finish(self) -> None:
        """
        Called when user finished writing his input (pressed enter)
        :return:
        """
        print(self.text)

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

        pygame.draw.line(screen, color, (x, self.y * 1.01), (x, self.y * 0.99 + self.h), 2)

    def draw(self, screen):
        """
        Draws input box, text and focus bar
        :param screen:
        :return:
        """
        # draw box
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))

        # Vertical Border Lines
        pygame.draw.line(screen, self.border_color, (self.x, self.y), (self.x, self.y + self.h),
                         self.border_width)
        pygame.draw.line(screen, self.border_color, (self.x + self.w, self.y), (self.x + self.w, self.y + self.h),
                         self.border_width)
        # Horizontal Border Lines
        pygame.draw.line(screen, self.border_color, (self.x, self.y), (self.x + self.w, self.y),
                         self.border_width)
        pygame.draw.line(screen, self.border_color, (self.x, self.y + self.h), (self.x + self.w, self.y + self.h),
                         self.border_width)

        # render text
        data = self.font.render(self.text, True, self.text_color)
        data_rect = data.get_rect()
        data_rect.midleft = self.rect.midleft[0] + self.padding, self.rect.midleft[1]

        # count time for focus color switch
        if self.hover:
            self.time += self.clock.tick()

        # self.time is in milliseconds so we multiply focus interval by 1000
        if self.time > self.focus_interval * 1000:
            # swap color between black and white
            self.focus_color = tuple(c ^ 255 for c in self.focus_color)
            self.time = 0

        self._draw_focus(screen, self.focus_color)
        screen.blit(data, data_rect)




    def update(self, event: pygame.event) -> None:
        """
        Updates the input box every frame
        :param event: current user event
        :return: None
        """
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
                if event.key == pygame.K_RETURN:
                    self._finish()
                elif event.key == pygame.K_BACKSPACE:
                    self.index = max(0, self.index - 1)
                    self.text = self.text[:self.index] + self.text[self.index + 1:]
                elif event.key == pygame.K_LEFT:
                    self.index = max(0, self.index - 1)
                elif event.key == pygame.K_RIGHT:
                    self.index = min(len(self.text), self.index + 1)
                else:
                    # Check if can add a new letter
                    new_width = self.font.render(self.text + event.unicode, True, self.text_color).get_rect()
                    if new_width.w < self.w - self.padding * 2:
                        self.index += 1
                        self.text = self.text[:self.index - 1] + event.unicode + self.text[self.index - 1:]
