import pygame
import numpy as np
import threading
import time
from UI.canvas import Canvas
from UI.button import Button
from UI.input_box import InputBox
from UI.timer import Timer
from file_parser import FileParser
from NeuralNetwork.neural_network import NeuralNetwork
from NeuralNetwork.layers import Convolutional, Pooling, Flatten, Dense, Dropout
from NeuralNetwork.activations import Relu, Softmax, Sigmoid
from NeuralNetwork.losses import CrossEntropyLoss
from NeuralNetwork.optimizers import Adam

from GameStates.menu_state import MenuState

from matplotlib import pyplot as plt


def predict(network, canvas):
    t = canvas.capture()
    if t is not None:
        print(network.objects[np.argmax(network.predict(t))])

def run_ai(network, clock, canvas):

    while True:
        t = canvas.capture()

        if t is not None:
            print(network.objects[np.argmax(network.predict(t))])

        time.sleep(3)

def main():
 
    pygame.font.init()
    background_colour = (122, 122, 122)
    screen = pygame.display.set_mode((1000, 800))

    pygame.display.set_caption('Scribble')
    screen.fill(background_colour)

    menu_screen = MenuState(screen)
    state = menu_screen.state
    """
    while True:
    
        if state == menu_screen.state:
            menu_screen.run()
            state = menu_screen.state
        else:
            print("jump")


        pygame.display.flip()
    """

    bg_pattern = pygame.image.load('images/pattern.png')
    screen.blit(bg_pattern, (0, 0))

    logo = pygame.image.load('images/logo.png')
    screen.blit(logo, ((1000 - 338) // 2, 10))

    canvas = Canvas(screen, 150, 150, 700, 500)
    file_parser = FileParser()



    train_x, train_y, test_x, test_y = file_parser.load(train_amount=50, test_amount=20)

    clock = pygame.time.Clock()
    clock.tick(60)
    total_time = 0
    idx = 0
    network = NeuralNetwork(
        [
            Convolutional(filters_num=2, filter_size=5, channels=1),
            Relu(),
            Pooling(filter_size=2, stride=2),
            Convolutional(filters_num=4, filter_size=3, channels=2),
            Relu(),
            Pooling(filter_size=2, stride=2),
            Flatten(),
            Dense(100, 2),
            Relu(),
            Dropout(0.4),
            Softmax()
        ],

        loss=CrossEntropyLoss(),
        optimizer=Adam(3e-04),
        objects=file_parser.files
        )

    network.train(train_x, train_y, test_x, test_y, epochs=1000, learning_rate=3e-4)
    network.save("NeuralNetwork/Models/10_new")


    # Adding buttons to the screen
    img = pygame.image.load("images/eraser.png")
    buttons = [
        Button((880, 560, 100, 40), image=img, color=(235, 232, 232), hover_color=(196, 191, 191), on_click=canvas.fill),
        Button((880, 610, 100, 40), text="predict", on_click= lambda: print(network.objects[np.argmax(network.predict(canvas.capture()))]))
    ]
    input_boxes = [
        InputBox((880, 510, 100, 40))
    ]
    timers = [
        Timer((880, 200, 100, 40), '00h:01m:05s', color=(125, 125, 125), text_color= (100, 255, 100), border_width= 0)
    ]


    clock = pygame.time.Clock()

    thread = threading.Thread(target=run_ai, args=(network, clock, canvas))
    thread.start()
    running = True
    while running:
        dt = clock.tick()
        for event in pygame.event.get():
            canvas.update(event)

            for button in buttons:
                button.handle_event(event)

            for input_box in input_boxes:
                input_box.handle_event(event)

            for timer in timers:
                timer.handle_event(event)

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

        total_time += dt
        if total_time > 5 * 1000:
            #predict(network, canvas)
            total_time = 0
        pygame.display.flip()


if __name__ == '__main__':
   main()

"""

game states=
menu, singleplayer, multiplayer

game_state = menu
while running:
    game_manager.run()



"""