import random
import struct
import numpy as np
from struct import unpack


class FileParser:

    def __init__(self):

        self.filenames = [
            'arm.bin',
            'dog.bin',
            'sun.bin'
        ]

        self.data = []
        self.percent = 0.8

    def load(self, filename, max_amount=1000):

        sets = []
        counter = 0

        with open(f'data/{filename}', 'rb') as file:
            while counter < max_amount:
                data = unpack_drawing(file, filename)
                # Skip drawings that have not been recognized by Google A.I
                if data['recognized']:
                    image = data['image']
                    label = np.zeros(len(self.filenames), dtype=int)
                    label[self.filenames.index(data['label'])] = 1

                    sets.append((image, label))
                    counter += 1

        return sets

    def load_all(self, seed=99):
        np.random.seed(seed)
        for filename in self.filenames:

            # Get image and label of drawing in binary file
            sets = self.load(filename)
            self.data += sets

        # Split data into training and test
        length = len(self.data)
        t_length = int(length * self.percent)

        training = np.array(self.data[:t_length])
        test = np.array(self.data[t_length:])

        # randomly shuffle array
        np.random.shuffle(training)
        np.random.shuffle(test)

        """
            Currently training, test shape is (N, 2) and training[n][0] = image, training[n][1] = label.
            In order to split the data into separate images, labels array, we transpose the matrix->
            The new shape will be (2, N) and training[0] = all images, training[1] = all labels
        """
        return *training.transpose(), *test.transpose()











def unpack_drawing(file_handle, label):
    # Read all data in file as mentioned in https://github.com/googlecreativelab/quickdraw-dataset
    key_id, = unpack('Q', file_handle.read(8))
    country_code, = unpack('2s', file_handle.read(2))
    recognized, = unpack('b', file_handle.read(1))
    timestamp, = unpack('I', file_handle.read(4))
    n_strokes, = unpack('H', file_handle.read(2))

    # Create image from pixels
    image = np.zeros(shape=(256, 256), dtype=int)
    # Loop through all strokes
    for i in range(n_strokes):
        # Unpack each stroke
        n_points, = unpack('H', file_handle.read(2))
        fmt = str(n_points) + 'B'
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
















