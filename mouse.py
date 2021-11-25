import pygame

class Mouse:

    def __init__(self, pos, stroke_width=1):

        self.pos = pos
        self.prev_pos = pos
        self.stroke_width = stroke_width

        self.pressed = False


    def update(self):

        self.prev_pos = self.pos
        self.pos = pygame.mouse.get_pos()

        self.pressed = pygame.mouse.get_pressed()[0]

        # If mouse has been released then no need to save previous position
        if self.pressed is False:
            self.prev_pos = self.pos
