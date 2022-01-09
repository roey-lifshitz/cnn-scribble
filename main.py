import pygame

from binary_file_parser import BinaryFileParser
from canvas import Canvas
from mouse import Mouse

def main():

    background_colour = (255, 255, 255)
    (width, height) = (800, 800)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Scribble')
    screen.fill(background_colour)

    canvas = Canvas(screen, 0, 0, 800, 800)
    mouse = Mouse(3)

    #parser = BinaryFileParser()
    #image = parser.load()


    running = True
    add = False
    while running:

        mouse.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if mouse.pressed:
                if canvas.contains(*mouse.pos):
                    add = True
                    canvas.draw_line(mouse.pos, mouse.prev_pos, mouse.radius)
            else:
                if add:
                    # When mouse is released, add latest line points into the data of canvas
                    canvas.add_line()
                    add = False



            if pygame.mouse.get_pressed()[2]:
                print(canvas.data)

        pygame.display.update()
        pygame.display.flip()


if __name__ == '__main__':
   main()