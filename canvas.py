import pygame
import algorithms
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Canvas:

    def __init__(self, screen, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.line = []
        self.data = []
        self.screen = screen.subsurface(x, y, width, height)

    # Check if given position is inside the canvas
    def contains(self, x, y):
        in_x_axis = self.x < x < self.x + self.width
        in_y_axis = self.y < y < self.y + self.height
        return in_x_axis and in_y_axis

    def clear(self):
        self.line = []
        self.data = []
        self.screen.fill(WHITE)

    def draw_line(self, start, end, radius):
        # Draw Line
        pygame.draw.line(self.screen, BLACK, start, end, radius)

        # Add points creating the line into self.points
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

    def save_line(self):

        # Compress the data into less points using the Douglas Peucker algorithm
        if len(self.line) > 0:

            # Algorithm receives [(x1, y1), (x2, y2), (x3, y3)]
            self.line = algorithms.douglas_peucker(self.line, 2.0)

            # Add to data
            self.data.append(self.line)

            # reset points
            self.line = []

    def prepare_data(self):

        rect = algorithms.bounds(self.data)
        print("RECT", rect)
        tmp = self.data
        self.data = algorithms.relocate(self.data, rect)
        self.draw_data(2)
        self.data = tmp

    def draw_data(self, radius):

        for line in self.data:
            for point in line:
                pygame.draw.circle(self.screen, BLACK, point, radius)





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
