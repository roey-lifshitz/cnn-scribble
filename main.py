import pygame
import numpy as np
from Ui.canvas import Canvas
from Ui.button import Button
from Ui.input_box import InputBox
from Ui.timer import Timer
from file_parser import FileParser
from NeuralNetwork.neural_network import NeuralNetwork
from NeuralNetwork.layers import Convolutional, Pooling, Flatten, Dense, Dropout
from NeuralNetwork.activations import Relu, Softmax, Sigmoid
from NeuralNetwork.losses import CrossEntropyLoss
from NeuralNetwork.optimizers import Adam

from matplotlib import pyplot as plt

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
    train_x, train_y, test_x, test_y = file_parser.load(train_amount=200, test_amount=40)

    clock = pygame.time.Clock()
    clock.tick(60)

    idx = 0
    network = NeuralNetwork(
        [
            Convolutional(filters_num=8, filter_size=5, channels=1),
            Relu(),
            Pooling(filter_size=2, stride=2),
            #Convolutional(filters_num=4, filter_size=5, channels=2),
            #Relu(),
            Pooling(filter_size=2, stride=2),
            Flatten(),
            Dense(218, 5),
            Softmax()
        ],
        loss=CrossEntropyLoss(),
        optimizer=None,
        objects=file_parser.files
        )

    #network.train(train_x, train_y, test_x, test_y, epochs=100, learning_rate=0.01)
    #network.save("NeuralNetwork/Models/5items.pkl")
    network.load("NeuralNetwork/Models/5items.pkl")
    #network.train(train_x, train_y, test_x, test_y, epochs=400, learning_rate=0.01)
    #network.save("NeuralNetwork/Models/5items2.pkl")


    #network.compute_graph()

    # Adding buttons to the screen
    img = pygame.image.load("images/eraser.png")
    buttons = [
        Button((880, 560, 100, 40), image=img, on_click=canvas.fill),
        Button((880, 610, 100, 40), text="predict", on_click= lambda: print(file_parser.files[np.argmax(network.predict(canvas.capture()))]))
    ]
    input_boxes = [
        InputBox((880, 510, 100, 40))
    ]
    timers = [
        Timer((880, 1000, 100, 40), '0h:0m:20s')
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
