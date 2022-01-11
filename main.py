import pygame

from binary_file_parser import BinaryFileParser
from canvas import Canvas
from mouse import Mouse

def main():

    background_colour = (255, 255, 255)
    (width, height) = (600, 600)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Scribble')
    screen.fill(background_colour)

    canvas = Canvas(screen, 0, 0, 600, 600)
    mouse = Mouse(pygame.mouse.get_pos(), 2)

    parser = BinaryFileParser()
    image = parser.load(screen, canvas)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    screen.fill((255, 255, 255))
                if event.key == pygame.K_p:
                    canvas.draw_data(screen, mouse.radius)

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse.pressed = False
                mouse.prev_pos = None
                canvas.save_points()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse.pressed = True

            elif event.type == pygame.MOUSEMOTION:
                if mouse.pressed:
                    mouse.pos = pygame.mouse.get_pos()
                    if mouse.prev_pos is not None:
                        canvas.draw_line(mouse.prev_pos, mouse.pos, mouse.radius)
                    mouse.prev_pos = mouse.pos

            if pygame.mouse.get_pressed()[2]:
                print(canvas.data)



        pygame.display.update()
        pygame.display.flip()


if __name__ == '__main__':
   main()
