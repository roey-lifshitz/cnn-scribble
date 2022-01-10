import pygame

class Mouse:

    def __init__(self, pos, radius=1):

        self.pos = pos
        self.prev_pos = None
        self.radius = radius

        self.pressed = False


    def update(self):

        if self.pressed:
            self.pos = pygame.mouse.get_pos()

