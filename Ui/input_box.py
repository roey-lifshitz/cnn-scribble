import pygame
import types


"""
Need to fix padding
"""
GRAY = (235, 232, 232)
HOVER_GRAY = (196, 191, 191)
BLACK = (0, 0, 0)


class InputBox:

    def __init__(self, rect,
                 padding: int = 10,
                 font="Ariel",
                 font_size=30,
                 color=GRAY,
                 border_color=BLACK,
                 border_width=2,
                 ):

        self.padding = padding
        self.color = color

        self.border_color = border_color
        self.border_width = border_width

        self.text = ""
        self.index = 0
        self.hover = False
        self.max_amount = None


        # Get the rect of the button
        self.x, self.y, self.w, self.h = rect
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        # Prepare what to draw
        self.font = pygame.font.SysFont(font, font_size)

        # Line to the right of last char in InputBox
        top = self.x, self.y
        bottom = self.x, self.y + self.h
        self.point = [top, bottom]

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

        data = self.font.render(self.text, True, BLACK)
        data_rect = data.get_rect()
        data_rect.midleft = self.rect.midleft[0] + self.padding, self.rect.midleft[1]

        if data_rect.right > self.rect.right:

            if not self.max_amount:
                self.max_amount = self.w // (data_rect.w // len(self.text))

            data = self.font.render(self.text[self.index:self.index + self.max_amount], True, BLACK)
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
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    # remove last letter
                    self.text = self.text[:-1]
                    self.index = max(0, self.index - 1)
                elif event.key == pygame.K_LEFT:
                    self.index = max(0, self.index - 1)

                elif event.key == pygame.K_RIGHT:
                    # amount of letters is bigger that amount of letter that u can display
                    if self.max_amount and self.index < len(self.text) - self.max_amount:
                        if len(self.text) >= self.max_amount:
                            self.index += 1
                else:
                    if self.max_amount:
                        if len(self.text) >= self.max_amount:
                            self.index += 1
                    self.text += event.unicode


