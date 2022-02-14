import pygame
import algorithms
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Canvas:

    def __init__(self, screen, x, y, width, height):
        # Rect of canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.line = []
        self.data = []

        # if we draw to self.screen in position (0, 0) it will draw to the pygame.screen in pos (self.x, self.y)
        # because self.screen is a sub screen of pygame.screen
        self.screen = screen.subsurface(x, y, width, height)

    def contains(self, x, y):
        """
        Check if self contains given coordinates
        :param x: x position
        :param y: y position
        :return: boolean if contains
        """
        in_x_axis = self.x < x < self.x + self.width
        in_y_axis = self.y < y < self.y + self.height
        return in_x_axis and in_y_axis

    def clear(self):
        """
        Clears all pixels of canvas and all data stored in canvas
        :return: None
        """
        # Clear data
        self.line = []
        self.data = []
        # Clear pixels
        self.screen.fill(WHITE)

    def draw_line(self, start, end, width):
        """
        Draws a line between to given dots, stores all dots that create the line
        :param start: line start position
        :param end: line end position
        :param width: width of line
        :return:
        """
        # Draw Line
        pygame.draw.line(self.screen, BLACK, start, end, width)

        x, y = start
        end_x, end_y = end

        # Calculate amount of points in line
        steps = max(abs(x - end_x), abs(y - end_y))

        # Calculate the offset between each point
        dx = (x - end_x) / steps
        dy = (y - end_y) / steps

        # Loop through points
        for _ in range(steps):
            # Add to Points List
            self.line.append((round(x), round(y)))
            # Update point
            x += dx
            y += dy


    def append_line(self):

        # if line not empty
        if len(self.line):
            print(self.line)
            # Compress the data into less points using the Douglas Peucker algorithm
            # Algorithm receives [(x1, y1), (x2, y2), (x3, y3)]
            self.line = algorithms.douglas_peucker(self.line, 2.0)
            print(self.line)
            # Add to data
            self.data.append(self.line)

            # reset points
            self.line = []

    def get_data(self):

        # get rect of drawing
        rect = algorithms.bounds(self.data)

        # Align Data to (0, 0)
        self.data = algorithms.relocate(self.data, rect)

        # Scale Drawing to maximum value of 255
        self.data, rect = algorithms.rescale(self.data, rect)

        # create pixel array pixels[256][256] = 0
        pixels = [[0] * 256] * 256
        # loop through lines
        for line in self.data:
            # loop through points
            for point in line:
                pixels[point[0]][point[1]] = 1

        # draw data on screen with 2 as radius of each point
        self.draw_data(2)
        return pixels

    def draw_data(self, radius):
        """
        Draws point on screen for each point in self.data
        :param radius: radius of points
        :return: None
        """
        for line in self.data:
            for point in line:
                pygame.draw.circle(self.screen, BLACK, point, radius)


    # Temp function just to check everything is okay
    def draw_loaded_data(self, data, radius):
        """
        Draws points on screen from loaded data
        :param data: pixel matrix
        :param radius:
        :return:
        """
        self.clear()
        for i in range(len(data)):
            for j in range(len(data)):
                # if point in pixel
                if data[i][j] == 1:
                    pygame.draw.circle(self.screen, BLACK, (i, j), radius)





    """
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
    """
