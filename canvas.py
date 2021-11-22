import pygame
import numpy as np
class canvas:



    def __init__(self, screen, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.screen = screen.subsurface(x, y, width, height)

    def contains(self, x, y):
        # check if given position is in bounds of Canvas
        in_x_axis = self.x < x and self.x + self.width > x
        in_y_axis = self.y < y and self.y + self.height > y
        return in_x_axis and in_y_axis

    def draw(self, x, y):
        #pygame.draw.rect(self.window, (0, 0, 0), (x, y, 1, 1), 5)
        self.screen.set_at((x - self.x, y - self.y), (0, 0, 0))

    def data(self):
        return pygame.surfarray.array3d(self.screen)


