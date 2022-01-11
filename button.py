import pygame
GRAY = (235, 232, 232)
HOVER_GRAY = (196, 191, 191)

class Button(pygame.sprite.Sprite()):

    def __init__(self, pos, size,
                 text = "Undefined",
                 font = "Ariel",
                 color=GRAY,
                 hover_color= HOVER_GRAY,
                 command=lambda: print("No command activated for this button")):
        # Child of pygame.Sprite
        super().__init__()
        self.text = text
        self.command = command
        self.color = color
        self.hover_color = color
        self.font = pygame.font.SysFont(font, size)
        self.render()
        # Design of button

    def render(self):
        self.text_render = self.font.render(self.text, 1, self.fg)



