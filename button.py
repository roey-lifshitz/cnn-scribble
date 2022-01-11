import pygame
GRAY = (235, 232, 232)
HOVER_GRAY = (196, 191, 191)
BLACK = (0, 0, 0)

class Button():

    def __init__(self, pos, size,
                 text="Undefined",
                 font="Ariel",
                 font_size=30,
                 color=GRAY,
                 hover_color=HOVER_GRAY,
                 border_color=BLACK,
                 border_width=2,
                 on_click=lambda: print("No command activated for this button")):
        # Child of pygame.Sprite
        super().__init__()

        self.on_click = on_click
        self.color = color
        self.hover_color = hover_color
        self.border_color = border_color
        self.border_width = border_width

        self.font = pygame.font.SysFont(font, font_size)
        self.text = self.font.render(text, True, BLACK)

        self.hover = False

        self.x, self.y, self.w, self.h = *pos, *size
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

    def draw(self, screen):
        """
        Draw 4 lines around the button and then fill them with color
        :return:
        """
        # Rect between lines
        if not self.hover:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
        else:
            pygame.draw.rect(screen, self.hover_color, (self.x, self.y, self.w, self.h))

        # Vertical Lines
        pygame.draw.line(screen, self.border_color, (self.x, self.y), (self.x, self.y + self.h),
                         self.border_width)
        pygame.draw.line(screen, self.border_color, (self.x + self.w, self.y), (self.x + self.w, self.y + self.h),
                         self.border_width)
        # Horizontal Lines
        pygame.draw.line(screen, self.border_color, (self.x, self.y), (self.x + self.w, self.y),
                         self.border_width)
        pygame.draw.line(screen, self.border_color, (self.x, self.y + self.h), (self.x + self.w, self.y + self.h),
                         self.border_width)

        # Draw text
        screen.blit(self.text, self.text_rect)

    def on_hover(self, mouse_pos):
        if self.rect.contains(pygame.Rect(*mouse_pos, 1, 1)):
            self.hover = True
            return True
        self.hover = False
        return False



    def click(self, mouse_pos):
        if self.rect.contains(pygame.Rect(*mouse_pos, 1, 1)):
            self.hover = False
            self.on_click()
            return True
        return False



