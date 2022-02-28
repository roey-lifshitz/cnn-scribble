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
    """
    file_parser = FileParser()
    train_x, train_y, test_x, test_y = file_parser.load(train_amount=1000, test_amount=200)

    clock = pygame.time.Clock()
    clock.tick(60)

    idx = 0
    network = NeuralNetwork(
        [
            Convolutional(filters_num=12, filter_size=5, channels=1),
            Relu(),
            Pooling(filter_size=2, stride=2),
            Convolutional(filters_num=24, filter_size=5, channels=12),
            Relu(),
            Pooling(filter_size=2, stride=2),
            Flatten(),
            Dense(384, 128),
            Dropout(0.6),
            Dense(128, 10),
            Softmax()
        ],
        loss=CrossEntropyLoss(),
        optimizer=None,
        objects=file_parser.files
        )
    #network.load("NeuralNetwork/Models/tmpaa1.pkl")
    #network.train(train_x, train_y, test_x, test_y, epochs=500, learning_rate=1e-3)
    #network.load("NeuralNetwork/Models/10items.pkl")

    #network.compute_graph()
    """
    # Adding buttons to the screen
    img = pygame.image.load("images/eraser.png")
    buttons = [
        Button((880, 560, 100, 40), image=img, on_click=canvas.fill),
        #Button((880, 610, 100, 40), text="predict", on_click= lambda: print(network.files[np.argmax(network.predict(canvas.capture()))]))
    ]
    input_boxes = [
        InputBox((880, 510, 100, 40))
    ]
    timers = [
        Timer((0, 100, 100, 40), '00h:01m:5s', color=(156, 152, 152), text_color=(134, 255, 129))
    ]

    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            canvas.update(event)

            for button in buttons:
                button.update(event)

            for input_box in input_boxes:
                input_box.update(event)

            for timer in timers:
                timer.update()

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    idx += 1
                    if idx == 24: idx = 0

        for button in buttons:
            button.draw(screen)

        for input_box in input_boxes:
            input_box.draw(screen, dt)

        for timer in timers:
            timer.draw(screen, dt)


        pygame.display.flip()


if __name__ == '__main__':
   main()
