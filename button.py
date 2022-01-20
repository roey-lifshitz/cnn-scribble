import pygame
GRAY = (235, 232, 232)
HOVER_GRAY = (196, 191, 191)
BLACK = (0, 0, 0)

""""
    Button Class
    This class represents an editable button that can be added into a pygame screen
"""
class Button:

    def __init__(self, pos, size,
                 text=None,
                 font="Ariel",
                 font_size=30,
                 image=None,
                 color=GRAY,
                 hover_color=HOVER_GRAY,
                 border_color=BLACK,
                 border_width=2,
                 on_click=lambda: print("No command activated for this button")):

        self.on_click = on_click
        self.color = color

        self.hover_color = hover_color
        self.border_color = border_color
        self.border_width = border_width

        self.hover = False

        # Get the rect of the button
        self.x, self.y, self.w, self.h = *pos, *size
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        # Button contains an image
        if image:
            self.data = image
        # Button contains a text
        elif text:
            font = pygame.font.SysFont(font, font_size)
            self.data = font.render(text, True, BLACK)

        self.data_rect = self.data.get_rect()

        # Center the image in relation to the button
        self.data_rect.center = self.rect.center

    def draw(self, screen):
        """
        Draw 4 lines (Border) around the button and then fill them with color
        :return:
        """
        # Rect between lines
        if not self.hover:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
        else:
            pygame.draw.rect(screen, self.hover_color, (self.x, self.y, self.w, self.h))

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

        # Draw data (inside button)
        screen.blit(self.data, self.data_rect)


    def check_hover(self, mouse_pos):
        """
        Check if mouse hovering on top of button
        """
        if self.rect.contains(pygame.Rect(*mouse_pos, 1, 1)):
            self.hover = True
            return True
        self.hover = False
        return False

    def check_click(self, mouse_pos):
        """
            Check if mouse clicking buton
        """
        if self.hover:
            self.hover = False
            self.on_click()
            return True
        return False



