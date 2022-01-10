import pygame
import algorithms
BLACK = (0, 0, 0)



class Canvas:

    def __init__(self, screen, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.points = [[], []]
        self.data = []
        self.screen = screen.subsurface(x, y, width, height)

    # Check if given position is inside the canvas
    def contains(self, x, y):
        in_x_axis = self.x < x < self.x + self.width
        in_y_axis = self.y < y < self.y + self.height
        return in_x_axis and in_y_axis

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
            self.points[0].append(round(x))
            self.points[1].append(round(y))
            # Update point
            x += dx
            y += dy

    def save_points(self):

        # Compress the data into less points using the Douglas Peucker algorithm
        if self.points[0]:
            print(self.points)
            # Algorithm receives [(x1, y1), (x2, y2), (x3, y3)]
            self.points = algorithms.douglas_peucker(list(zip(*self.points)), 2.0)

            # turn self.points = [[x1, x2, x3], [y1, y2, y3]]
            self.points = [[x for x, y in self.points], [y for x, y, in self.points]]

            # Add to data
            self.data.append(list(self.points))

            # reset points
            self.points = [[], []]

    def draw_data(self, screen, radius):

        for line in self.data:
            for x, y in list(zip(*line)):
                pygame.draw.circle(screen, BLACK, (x, y), radius)





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
