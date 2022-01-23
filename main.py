import pygame
from canvas import Canvas
from mouse import Mouse
from button import Button
from FileParser import FileParser
from NeuralNetwork import NeuralNetwork

def main():
    pygame.font.init()

    background_colour = (255, 255, 255)
    (width, height) = (600, 600)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Scribble')
    screen.fill(background_colour)

    canvas = Canvas(screen, 0, 0, 500, 500)
    mouse = Mouse(pygame.mouse.get_pos(), 2)

    file_parser = FileParser()
    train_x, train_y, test_x, test_y = file_parser.load_all()
    print(len(train_y), len(test_y))


    # Adding buttons to the screen
    img = pygame.image.load("images/eraser.png")
    buttons = []
    b1 = Button((540, 550), (50, 40), image=img, on_click=canvas.clear)
    b2 = Button((540, 500), (50, 40), text="dots", on_click=lambda: canvas.draw_data(mouse.radius))
    b3 = Button((540, 450), (50, 40), text="show", on_click=canvas.get_data)
    buttons.append(b1)
    buttons.append(b2)
    buttons.append(b3)


    running = True
    while running:
        mouse.pos = pygame.mouse.get_pos()

        for button in buttons:
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                pass

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse.pressed = False
                mouse.prev_pos = None
                canvas.append_line()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse.pressed = True

                for button in buttons:
                    if button.check_click(mouse.pos):
                        pass

            elif event.type == pygame.MOUSEMOTION:
                if mouse.pressed:
                    if canvas.contains(*mouse.pos) and mouse.prev_pos is not None:
                        canvas.draw_line(mouse.prev_pos, mouse.pos, mouse.radius)
                    mouse.prev_pos = mouse.pos

            if not mouse.pressed:
                for button in buttons:
                    if button.check_hover(mouse.pos):
                        pass

        pygame.display.update()
        pygame.display.flip()


if __name__ == '__main__':
   main()