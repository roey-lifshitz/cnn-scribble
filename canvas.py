import pygame
import numpy as np


BLACK = (0, 0, 0)


class Canvas:
    def __init__(self, screen, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


        self.strokes = [(), ()]
        self.screen = screen.subsurface(x, y, width, height)

    # Check if given position is inside the canvas
    def contains(self, x, y):
        in_x_axis = self.x < x and self.x + self.width > x
        in_y_axis = self.y < y and self.y + self.height > y
        return in_x_axis and in_y_axis

    # Draws a line in a given position
    def draw(self, pos, prev_pos, radius):

        if prev_pos == pos:
            pygame.draw.circle(self.screen, BLACK, pos, radius)
            self.strokes[0] += (pos[0], )
            self.strokes[1] += (pos[1], )
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
                self.strokes[0] += (round(prev_x), )
                self.strokes[1] += (round(prev_y), )
                pygame.draw.circle(self.screen, BLACK, (round(prev_x), round(prev_y)), radius)

    def get_strokes(self):
        return self.strokes


    def to_binary(self):
        # returns a serialized 3d array- maybe for later if we want to include colors in drawings
        image = pygame.surfarray.array3d(self.screen)
        # reshape it into one dimensional array
        pixels = image.ravel()
        # slice it to receive only red value of every pixel start:stop:step
        pixels = pixels[::3]
        # turn every 225 to 0 and 0 to 1
        pixels[pixels == 0] = 1
        pixels[pixels == 255] = 0
        return pixels

    def load_scribble(self, pixels):
        self.screen.fill((255, 255, 255))
        print(pixels[0])
        for i in range(len(pixels[0][0])):
            pos = pixels[0][0][i], pixels[0][1][i]
            print(pos)
            pygame.draw.circle(self.screen, BLACK, pos, 1)
            self.screen.set_at(pos, BLACK)

        pygame.display.update()
        pygame.display.flip()

    """
       
         
        # Gray Scales the pixels
        grayscaled_pixels = np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])
         
         """