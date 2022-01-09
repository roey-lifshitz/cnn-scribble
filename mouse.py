import pygame
import numpy as np



class Mouse:

    def __init__(self, radius=1):

        self.radius = radius
        self.pos = pygame.mouse.get_pos()
        self.prev_pos = self.pos
        self.pressed = False

    def update(self):

        self.pressed = pygame.mouse.get_pressed()[0]
        self.prev_pos = self.pos
        self.pos = pygame.mouse.get_pos()






