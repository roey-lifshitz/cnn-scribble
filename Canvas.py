import pygame
import numpy as np
from matplotlib import pyplot as plt
from typing import Optional, Tuple
import Algorithms
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Canvas:
    """
        Drawing Board for a pygame display Surface.
    """
    def __init__(self, screen: pygame.Surface, x: int, y: int, width: int, height: int, colorful: bool = False) -> None:
        """
        Initialize function
        :param screen: display surface
        :param x: x of canvas
        :param y: y of canvas
        :param width: width of canvas
        :param height: height of canvas
        """
        # Rect of canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # if screen is only in black and white
        self.colorful = colorful

        # since self.screen is a sub screen of pygame.screen, if we draw to self.screen in position (0, 0)
        # it will draw to the display screen in pos (self.x, self.y)
        self.screen = screen.subsurface(x, y, width, height)

    def contains(self, x: int, y: int):
        """
        Check if coordinates are contained by the canvas
        :param x: x position
        :param y: y position
        :return: boolean if contains
        """
        in_x_axis = self.x < x < self.x + self.width
        in_y_axis = self.y < y < self.y + self.height
        return in_x_axis and in_y_axis

    def fill(self, color: Optional[Tuple[int, int, int]] = (255, 255, 255)) -> None:
        """
        Fills all canvas with a certain color
        By default fills with White
        :param color: r, g, b of color
        :return: None
        """

        self.screen.fill(color)

    def draw(self, start: Tuple[int, int], end: Tuple[int, int], radius: int,
             color: Optional[Tuple[int, int, int]] = (0, 0, 0)) -> None:
        """
        Draws a line between two given positions
        The line consists of many small circles
        By default draws with black
        :param start: x, y of start position
        :param end: x, y of end position
        :param radius: radius of circles to draw
        :param color: r, g, b of color
        :return: None
        """
        # Draw a point
        if start == end:
            pygame.draw.circle(self.screen, color, end, radius)
        else:
            # Draw a line

            x, y = start
            end_x, end_y = end

            # Calculate amount of points in line
            steps = max(abs(x - end_x), abs(y - end_y))

            # Calculate the offset between each point
            dx = (x - end_x) // steps
            dy = (y - end_y) // steps

            # Loop through points in line
            for _ in range(steps):
                # Draw point in line
                pygame.draw.circle(self.screen, color, (x, y), radius)
                # Update point
                x += dx
                y += dy

    def capture(self) -> np.ndarray:
        """
        Calculates a 1x28x28 numpy array representing the image on the canvas
        :return: array with shape (channels, width, height)
        """
        # return a (height, width , channels) representation of the canvas
        image = pygame.surfarray.array3d(self.screen)

        if self.colorful:
            # gray scale image (darker the pixel smaller the value)
            # we want to reverse the effect- darker the pixel bigger the value so we subtract the image from the max
            # possible value
            image = 255 - np.dot(image[..., :], [0.2989, 0.5870, 0.1140])

        else:
            # image only in black and white-> r, g, b of each pixel are the same (255 or 0)
            image = image[:, :, 0]

            # currently white is represented by 255 and black by 0
            # we want to swap that
            # 255 in binary = 0x1111 1111 | 0 in binary = 0x0000 0000
            # if we apply xor with 0x111 1111 then
            # white is represented with 0 and black is represented with 255
            image ^= 0b11111111

        # swap from (height, width) to (width, height)
        image = np.swapaxes(image, 0, 1)
        # normalize the image
        image = image.astype('float32') / 255.
        # crop all whitespace surrounding drawing in image
        image = Algorithms.crop_whitespaces(image)
        # pad image so width == height
        image = Algorithms.add_border(image, same_scale=True)
        # down sample to training data size for neural network
        image = Algorithms.down_sample(image, (28, 28))

        plt.imshow(image)
        plt.show()

        return image.reshape(1, 28, 28)

