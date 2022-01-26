import numpy as np
from struct import unpack


def unpack_drawing(file_handle, label):
    """
    Reads the data of a single drawing from google's quickdraw data set.
    The file it reads from consists of multiple drawings of the same object
    To read multiple objects all you need to do is call this function a number of times for the same file_handle
    https://github.com/googlecreativelab/quickdraw-dataset

    :param file_handle: File object
    :param label: label of drawing it is about to read
    :return: Dictionary {'label', 'recognized', 'image'}
    """

    # Read all data from current file object location
    key_id, = unpack('Q', file_handle.read(8))
    country_code, = unpack('2s', file_handle.read(2))
    recognized, = unpack('b', file_handle.read(1))
    timestamp, = unpack('I', file_handle.read(4))
    n_strokes, = unpack('H', file_handle.read(2))

    # Create matrix of pixels for the image
    image = np.zeros(shape=(256, 256), dtype=int)
    # Loop through all strokes
    for i in range(n_strokes):
        # Unpack each stroke
        n_points, = unpack('H', file_handle.read(2))
        fmt = str(n_points) + 'B'
        # x, y arrays of points that have been drawn p[0] = (x[0], y[0])
        x = unpack(fmt, file_handle.read(n_points))
        y = unpack(fmt, file_handle.read(n_points))
        # Add stroke to data
        for point in list(zip(x, y)):
            image[point] = 1

    return {
        'label': label,
        'recognized': recognized,
        'image': image
    }


class FileParser:

    def __init__(self):

        self.filenames = [
            'arm.bin',
            'dog.bin',
            'sun.bin'
        ]
        self.percent = 0.8

    def load(self, filename, amount):
        """
        Loads specified amount of drawings from a given file name
        :param filename: filename
        :param amount: amount of drawings to load
        :return: array of tuples, each tuple= (image, label)
        """
        sets = []
        counter = 0

        # Open binary file
        with open(f'data/{filename}', 'rb') as file:
            # Loop for specified amount
            while counter < amount:
                # unpack single drawing
                data = unpack_drawing(file, filename)
                # Skip drawings that have not been recognized by Google A.I
                # We don't want our network to study from images that Google A.I didn't recognize

                if data['recognized']:
                    image = data['image']
                    label = np.zeros(len(self.filenames), dtype=int)
                    label[self.filenames.index(data['label'])] = 1
                    sets.append((image, label))
                    counter += 1

        return sets

    def load_all(self, seed=99, amount=99):
        """
        Loads all drawings that appear in self.filename
        :param seed: optional, for numpy.random
        :return: train_x, train_y, test_x, test_y
        """
        np.random.seed(seed)
        all_sets = []
        # Loop through all filenames
        for filename in self.filenames:

            # Get (image, label) of drawings for specific filename
            sets = self.load(filename, amount)

            # array that contains all sets
            all_sets += sets

        # Calculate length of training data
        length = len(all_sets)
        t_length = int(length * self.percent)

        # Split data into training and test (80% training, 20% test)
        training = np.array(all_sets[:t_length])
        test = np.array(all_sets[t_length:])

        # randomly shuffle arrays
        np.random.shuffle(training)
        np.random.shuffle(test)

        """
            Currently, training and test shape is (N, 2) and training[0]= image, label
            In order to split the data into separate images and labels arrays
            we can transpose the matrix-> 
            The new shape will be (2, N) and training[0] = all images, training[1] = all labels
        """
        return *training.transpose(), *test.transpose()





















