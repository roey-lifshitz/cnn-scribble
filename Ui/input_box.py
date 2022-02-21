import pygame

class InputBox:
    """
    Static input box
    """
    def __init__(self, rect,
                 padding: int = 10,
                 font="Ariel",
                 font_size=30,
                 color=(255, 255, 255),
                 text_color= (0, 0, 0),
                 border_color=(0, 0, 0),
                 border_width=2,
                 ):

        self.padding = padding
        self.color = color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.focus_color = (0, 0, 0)

        self.font = pygame.font.SysFont(font, font_size)
        self.clock = None
        self.time = -1
        self.hover = False

        # Get the rect of the button
        self.x, self.y, self.w, self.h = rect
        self.rect = pygame.Rect(rect)

        self.text = ""
        self.index = 0

    def _finish(self):
        print(self.text)

    def _draw_focus(self):
        # Swap color between white and black evry 2 seconds
        print(self.time)
        if self.time % 2000 == 0:
            self.time = -1
            self.focus_color = tuple(c ^ 255 for c in self.focus_color)
            print(self.focus_color)

    def draw(self, screen):

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

        data = self.font.render(self.text, True, self.text_color)
        data_rect = data.get_rect()
        data_rect.midleft = self.rect.midleft[0] + self.padding, self.rect.midleft[1]

        screen.blit(data, data_rect)
        self._draw_focus()

    def update(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(*pygame.mouse.get_pos()):
                self.hover = True
                self.clock = pygame.time.Clock()
            # Continue writing until clicked again
            else:
                self.hover = False
                self.clock = None
                self.time = -1

        if self.hover:
            self.time += self.clock.tick()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._finish()
                elif event.key == pygame.K_BACKSPACE:
                    self.index = max(0, self.index - 1)
                    self.text = self.text[:self.index] + self.text[self.index + 1:]
                elif event.key == pygame.K_LEFT:
                    self.index = max(0, self.index - 1)
                elif event.key == pygame.K_RIGHT:
                    self.index = min(len(self.text), len(self.text) + 1)
                else:
                    # Check if can add a new letter
                    new_width = self.font.render(self.text + event.unicode, True, self.text_color).get_rect()
                    if new_width.w < self.w - self.padding * 2:
                        self.index += 1
                        self.text += event.unicode


