
from file_parser import FileParser
from NeuralNetwork.model import Model
from NeuralNetwork.layers import Convolutional, Pooling, Flatten, Dense, Dropout
from NeuralNetwork.activations import Relu, Softmax, Sigmoid
from NeuralNetwork.losses import CrossEntropyLoss
from NeuralNetwork.optimizers import Adam, GradientDescent


def main():
 
    file_parser = FileParser()
    train_x, train_y, test_x, test_y = file_parser.load(train_amount=100, test_amount=20)

    network = Model(
        [
            Convolutional(filters_num=2, filter_size=3, channels=1),
            Relu(),
            Pooling(filter_size=2, stride=2),
            Convolutional(filters_num=4, filter_size=3, channels=2),
            Relu(),
            Pooling(filter_size=2, stride=2),
            Flatten(),
            Dense(100, 2),
            Softmax()
        ],

        loss=CrossEntropyLoss(),
        optimizer=Adam(0.001),
        objects=file_parser.get_objects()
    )


    network.train(train_x, train_y, test_x, test_y, epochs=900)
    network.save("NeuralNetwork/Models/10_new")


if __name__ == '__main__':
   main()
