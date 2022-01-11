import pygame

from binary_file_parser import BinaryFileParser
from canvas import Canvas
from mouse import Mouse
from button import Button

def main():

    pygame.font.init()

    background_colour = (255, 255, 255)
    (width, height) = (600, 600)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Scribble')
    screen.fill(background_colour)

    canvas = Canvas(screen, 0, 0, 600, 600)
    mouse = Mouse(pygame.mouse.get_pos(), 2)

    parser = BinaryFileParser()
    image = parser.load(screen, canvas)

    img = pygame.image.load("images/eraser.png")
    buttons = []
    #b1 = Button((480, 550), (100, 30), text="Erase", on_click=lambda: canvas.clear())
    b1 = Button((480, 550), (50, 40), image=img, on_click=lambda: canvas.clear())
    b2 = Button((480, 440), (100, 30), text="Show rmd", on_click=lambda: canvas.draw_data(mouse.radius))
    buttons.append(b1)
    buttons.append(b2)


    running = True
    while running:
        mouse.pos = pygame.mouse.get_pos()
        for button in buttons:
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    screen.fill()
                    canvas.draw_data(mouse.radius)
                if event.key == pygame.K_o:
                    print(canvas.data)

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse.pressed = False
                mouse.prev_pos = None
                canvas.save_points()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse.pressed = True

                for button in buttons:
                    if button.click(mouse.pos):
                        pass

            elif event.type == pygame.MOUSEMOTION:
                if mouse.pressed:
                    if mouse.prev_pos is not None:
                        canvas.draw_line(mouse.prev_pos, mouse.pos, mouse.radius)
                    mouse.prev_pos = mouse.pos

            if not mouse.pressed:
                for button in buttons:
                    if button.on_hover(mouse.pos):
                        pass


        pygame.display.update()
        pygame.display.flip()


if __name__ == '__main__':
   main()