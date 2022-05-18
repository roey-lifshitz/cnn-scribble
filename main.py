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


def main():
 
    file_parser = FileParser()
    train_x, train_y, test_x, test_y = file_parser.load(train_amount=400, test_amount=50)

    network = NeuralNetwork(
        [
            Convolutional(filters_num=24, filter_size=5, channels=1),
            Relu(),
            Pooling(filter_size=2, stride=2),
            Convolutional(filters_num=48, filter_size=3, channels=24),
            Relu(),
            Pooling(filter_size=2, stride=2),
            Flatten(),
            Dropout(0.2),
            Dense(1200, 600),
            Relu(),
            Dense(600, 10),
            Softmax()
        ],

        loss=CrossEntropyLoss(),
        optimizer=Adam(3e-5),
        objects=file_parser.get_objects()
    )

    network.load("NeuralNetwork/Models/10_85.pkl")
    print(network.model)
    network.train(train_x, train_y, test_x, test_y, epochs=900)
    network.save("NeuralNetwork/Models/10_new")


if __name__ == '__main__':
   main()

"""

game states=
menu, singleplayer, multiplayer

game_state = menu
while running:
    game_manager.run()



"""