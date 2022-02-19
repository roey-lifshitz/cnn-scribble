import pygame
import numpy as np
from Ui.canvas import Canvas
from Ui.button import Button
from Ui.input_box import InputBox
from file_parser import FileParser
from neural_network import NeuralNetwork


def main():
 
    pygame.font.init()
    background_colour = (122, 122, 122)
    screen = pygame.display.set_mode((1000, 800))

    pygame.display.set_caption('Scribble')
    screen.fill(background_colour)

    bg_pattern = pygame.image.load('images/pattern.png')
    screen.blit(bg_pattern, (0, 0))

    logo = pygame.image.load('images/logo.png')
    screen.blit(logo, ((1000 - 338) // 2, 10))

    canvas = Canvas(screen, 150, 150, 700, 500)
    file_parser = FileParser()
    train_x, train_y, test_x, test_y = file_parser.load(train_amount=1000, test_amount=100)


    idx = 0
    network = NeuralNetwork()
    network.load("Models/4ItemsModelTmp.pkl")


    #"""
    # Adding buttons to the screen
    img = pygame.image.load("images/eraser.png")
    buttons = [
        Button((880, 560, 100, 40), image=img, on_click=canvas.fill),
        Button((880, 610, 100, 40), text="predict", on_click= lambda: print(file_parser.files[np.argmax(network.predict(canvas.capture()))]))
    ]
    input_boxes = [
        InputBox((880, 510, 100, 40))
    ]


    running = True
    while running:

        for event in pygame.event.get():

            canvas.update(event)

            for button in buttons:
                button.update(event)

            for input_box in input_boxes:
                input_box.update(event)

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    idx += 1
                    if idx == 24: idx = 0

        for button in buttons:
            button.draw(screen)

        for input_box in input_boxes:
            input_box.draw(screen)



        pygame.display.flip()


if __name__ == '__main__':
   main()
