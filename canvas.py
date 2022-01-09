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

        # Draw starting position
        pygame.draw.circle(self.screen, BLACK, start, radius)

        curr_x, curr_y = start
        self.points[0].append(round(curr_x))
        self.points[1].append(round(curr_y))

        # If drawn a line, meaning start isn't equal to end
        if start != end:
            end_x, end_y = end
            # Calculate amount of points in line
            steps = max(abs(curr_x - end_x), abs(curr_y - end_y))
            # Calculate the offset between each point
            dx = (curr_x - end_x) / steps
            dy = (curr_y - end_y) / steps

            # create list of all points
            for _ in range(steps):
                curr_x += dx
                curr_y += dy

                # Draw a dot to create an effect of a continuous stroke
                pygame.draw.circle(self.screen, BLACK, (round(curr_x), round(curr_y)), radius)
                self.points[0].append(round(curr_x))
                self.points[1].append(round(curr_y))

    def add_line(self):
        # compress the data into less points using the Douglas Peucker algorithm
        print(self.points)
        self.points = algorithms.douglas_peucker(self.points, 2.0)
        print("AFTER: ")
        print(self.points)
        self.data.append(self.points)
        self.points = [[], []]

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
