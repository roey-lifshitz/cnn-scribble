import pygame
import types

GRAY = (235, 232, 232)
HOVER_GRAY = (196, 191, 191)
BLACK = (0, 0, 0)


class InputBox:

    def __init__(self, rect,
                 font="Ariel",
                 font_size=30,
                 color=GRAY,
                 border_color=BLACK,
                 border_width=2,
                 ):

        self.color = color

        self.border_color = border_color
        self.border_width = border_width

        self.text = ""
        self.active = False
        self.send = False

        # Get the rect of the button
        self.x, self.y, self.w, self.h = rect
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        # Prepare what to draw
        self.font = pygame.font.SysFont(font, font_size)

        # Line to the right of last char in InputBox
        top = self.x, self.y
        bottom = self.x, self.y + self.h
        self.point = [top, bottom]

    def is_click(self, mouse_pos):
        if self.rect.contains(pygame.Rect(*mouse_pos, 1, 1)):
            self.active = True
            return True
        self.active = False
        return False

    def update_text(self, char):
        if self.active:

            if char == 13:  # Num of enter
                self.send = True

            elif char.isalpha() or char.isspace():
                self.text += char

    def get_text(self):

        if self.send:
            print(self.text)
            self.send = False
            tmp = self.text
            self.text = ""
            return tmp
        return ""

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

        # Update text displayed on text box
        data = self.font.render(self.text, True, BLACK)

        data_rect = data.get_rect()
        data_rect.center = self.rect.center
        screen.blit(data, data_rect)

