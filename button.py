import pygame
GRAY = (235, 232, 232)
HOVER_GRAY = (196, 191, 191)
BLACK = (0, 0, 0)

class Button(pygame.sprite.Sprite()):

    def __init__(self, pos, size,
                 text = "Undefined",
                 font = "Ariel",
                 color=GRAY,
                 hover_color= HOVER_GRAY,
                 border_color= BLACK,
                 border_width = 2,
                 command=lambda: print("No command activated for this button")):
        # Child of pygame.Sprite
        super().__init__()
        self.text = text
        self.command = command
        self.color = color
        self.hover_color = color
        self.border_color = border_color
        self.border_width = border_width
        self.font = pygame.font.SysFont(font, size)
        self.render()

        self.x, self.y, self.w, self.h = pos, size
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)


    def render(self):
        # Sets Sprtie.image
        self.image = self.font.render(self.text, 1, self.fg)

    def draw(self, screen):
        """
        Draw 4 lines around the button and then fill them with color
        :return:
        """
        # Vertical Lines
        pygame.draw.line(screen, self.border_color, (self.x, self.y), (self.x, self.y + self.h),
                         self.border_width)
        pygame.draw.line(screen, self.border_color, (self.x + self.w, self.y), (self.x + self.w, self.y + self.h),
                         self.border_width)
        # Horizontal Lines
        pygame.draw.line(screen, self.border_color, (self.x, self.y), (self.x + self.w, self.y),
                         self.border_width)
        pygame.draw.line(screen, self.border_color, (self.x + self.w, self.y), (self.x + self.w, self.y + self.h),
                         self.border_width)
        # Rect between lines
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))

