import pygame
import numpy as np
from Canvas import Canvas
from mouse import Mouse
from Ui.Button import Button
from FileParser import FileParser
from NeuralNetwork import NeuralNetwork
from matplotlib import pyplot as plt
def main():
 
    pygame.font.init()
    background_colour = (255, 255, 255)
    (width, height) = (600, 600)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Scribble')
    screen.fill(background_colour)

    canvas = Canvas(screen, 0, 0, 500, 500)
    mouse = Mouse(pygame.mouse.get_pos(), 4)
    file_parser = FileParser()
    train_x, train_y, test_x, test_y = file_parser.load(train_amount=1000, test_amount=100)

    plt.imshow(train_x[0][0])
    plt.show()

    idx = 0
    network = NeuralNetwork()
    network.load("Models/4ItemsModelTmp.pkl")


    #"""
    # Adding buttons to the screen
    img = pygame.image.load("images/eraser.png")
    buttons = [
        Button((540, 550, 50, 40), image=img, on_click=canvas.fill),
        Button((540, 450, 50, 40), text="predict", on_click= lambda: print(file_parser.files[np.argmax(network.predict(canvas.capture()))]))
    ]
     #b3 = Button((540, 450, 50, 40), text="load", on_click=lambda: canvas.draw_loaded_data(train_x[idx], 2))

    #buttons.append(b3)


    running = True
    while running:
        mouse.pos = pygame.mouse.get_pos()

        for button in buttons:
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    idx += 1
                    if idx == 24: idx = 0

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse.pressed = False
                mouse.prev_pos = None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse.pressed = True

                for button in buttons:
                    if button.click():
                        pass

            elif event.type == pygame.MOUSEMOTION:
                if mouse.pressed:
                    if canvas.contains(*mouse.pos) and mouse.prev_pos is not None:
                        canvas.draw(mouse.prev_pos, mouse.pos, mouse.radius)
                    mouse.prev_pos = mouse.pos

            if not mouse.pressed:
                for button in buttons:
                    if button.is_click(mouse.pos):
                        pass

        pygame.display.flip()


if __name__ == '__main__':
   main()
