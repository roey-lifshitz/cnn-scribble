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
    train_x, train_y, test_x, test_y = file_parser.load(train_amount=1000, test_amount=100)

    network = NeuralNetwork(
        [
            Convolutional(filters_num=32, filter_size=5, channels=1),
            Relu(),
            Pooling(filter_size=2, stride=2),
            Convolutional(filters_num=64, filter_size=3, channels=32),
            Relu(),
            Pooling(filter_size=2, stride=2),
            Flatten(),
            Dropout(0.2),
            Dense(1600, 600),
            Relu(),
            Dense(600, 100),
            Relu(),
            Dense(100, 26),
            Softmax()
        ],

        loss=CrossEntropyLoss(),
        optimizer=Adam(3e-5),
        objects=file_parser.get_objects()
    )

    network.load("NeuralNetwork/Models/temp.pkl")
    network.train(train_x, train_y, test_x, test_y, epochs=900)
    network.save("NeuralNetwork/Models/10_new")


if __name__ == '__main__':
   main()
