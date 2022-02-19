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

        self.font = pygame.font.SysFont(font, font_size)

        self.hover = False

        # Get the rect of the button
        self.x, self.y, self.w, self.h = rect
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        self.text = ""

    def _finish(self):
        print(self.text)

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

    def update(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(*pygame.mouse.get_pos()):
                self.hover = True
            # Continue writing until clicked again
            else:
                self.hover = False

        if self.hover:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._finish()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[0:-1]
                else:
                    # Check if can add a new letter
                    new_width = self.font.render(self.text + event.unicode, True, self.text_color).get_rect()
                    if new_width.w < self.w - self.padding * 2:
                        self.text += event.unicode


