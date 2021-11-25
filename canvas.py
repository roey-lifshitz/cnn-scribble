import pygame
import numpy as np


BLACK = (0, 0, 0)
class Canvas:

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

    def draw(self, pos, prev_pos, radius):

        if pos == prev_pos:
            pygame.draw.circle(self.screen, BLACK, pos, radius)
        else:
            # Draw circles between current mouse position and previous mouse position
            x, y = pos
            prev_x, prev_y = prev_pos
            # Calculate amount amount of points to add
            steps = max(abs(x - prev_x), abs(y - prev_y))
            # Calculate the offset of each point
            x_offset = (x - prev_x) / steps
            y_offset = (y - prev_y) / steps
            # Draw points
            for _ in range(steps):
                prev_x += x_offset
                prev_y += y_offset
                pygame.draw.circle(self.screen, BLACK, (round(prev_x), round(prev_y)), radius)

    def to_binary(self):
        # returns a serialized 3d array- maybe for later if we want to include colors in drawings
        pixels = pygame.surfarray.array3d(self.screen)
        # reshape it into one dimensional array
        pixels = pixels.ravel()
        # slice it to receive only red value of every pixel start:stop:step
        pixels = pixels[::3]
        # turn every 225 to 0 and 0 to 1
        pixels[pixels == 0] = 1
        pixels[pixels == 255] = 0
        return pixels

