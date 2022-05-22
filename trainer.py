
from file_parser import FileParser
from NeuralNetwork.model import Model
from NeuralNetwork.layers import Convolutional, Pooling, Flatten, Dense, Dropout
from NeuralNetwork.activations import Relu, Softmax, Sigmoid
from NeuralNetwork.losses import CrossEntropyLoss
from NeuralNetwork.optimizers import Adam


def main():
 
    file_parser = FileParser()
    train_x, train_y, test_x, test_y = file_parser.load(train_amount=26, test_amount=26)

    network = NeuralNetwork(
        [
            Convolutional(filters_num=16, filter_size=3, channels=1),
            Relu(),
            Pooling(filter_size=2, stride=2),
            Convolutional(filters_num=32, filter_size=3, channels=16),
            Relu(),
            Pooling(filter_size=2, stride=2),
            Convolutional(filters_num=64, filter_size=3, channels=32),
            Relu(),
            Flatten(),
            Dense(576, 256),
            Relu(),
            Dropout(0.2),
            Dense(256, 128),
            Relu(),
            Dropout(0.2),
            Dense(128, 26),
            Softmax()
        ],

        loss=CrossEntropyLoss(),
        optimizer=Adam(3e-5),
        objects=file_parser.get_objects()
    )


    network.train(train_x, train_y, test_x, test_y, epochs=900)
    network.save("NeuralNetwork/Models/10_new")


if __name__ == '__main__':
   main()
