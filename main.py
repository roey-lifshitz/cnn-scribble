import pygame

from canvas import canvas

def main():

    background_colour = (255, 255, 255)
    (width, height) = (600, 600)


    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Tutorial 1')
    screen.fill(background_colour)

    cnvs = canvas(screen, 0, 0, 100, 100)

    running = True
    draw = False
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if cnvs.contains(mouse_x, mouse_y):
                    cnvs.draw(mouse_x, mouse_y)

            if pygame.mouse.get_pressed()[2]:
                print(cnvs.data())

        pygame.display.update()
        pygame.display.flip()


if __name__ == '__main__':
   main()