import numpy as np

class FileParser:

    def __init__(self):

        self.filenames = [
            'apple.npy',
            'duck.npy',
            'foot.npy',
            'sun.npy'
        ]

    def load(self, train_amount: int = 300, test_amount: int = 50, seed: int = 99):

        if 0 < test_amount < len(self.filenames) or 0 < train_amount < len(self.filenames):

            raise ValueError("amount is smaller than files in Class, Cannot load less than one file per file")

        np.random.seed(seed)

        # Prepare variables for easier loading
        amount_of_files = len(self.filenames)
        train_amount_per_file = train_amount // amount_of_files
        test_amount_per_file = test_amount // amount_of_files
        offset = train_amount_per_file

        train_data = np.empty((train_amount, 2), dtype=object)
        test_data = np.empty((test_amount, 2), dtype=object)

        for i, filename in enumerate(self.filenames):

            # Load images from .npy file
            images = np.load(f"data/{filename}") / 255.
            # Reshape that each image will be in a 1X28X28 format
            images = images.reshape(-1, 1, 28, 28)

            # binary array that represents the location of the filename in self.filenames
            y = np.zeros(amount_of_files)
            y[i] = 1

            # Indices for storing data
            train_start = i * train_amount_per_file
            train_end = train_start + train_amount_per_file
            test_start = i * test_amount_per_file
            test_end = test_start + test_amount_per_file

            train_data[train_start:train_end] = list(zip(images[train_start:train_end], [y] * train_amount_per_file))
            test_data[test_start:test_end] = list(zip(images[test_start + offset:test_end + offset], [y] * test_amount_per_file))

        # Shuffle the array
        np.random.shuffle(train_data)
        np.random.shuffle(test_data)

        train_x, train_y = test_data.transpose()
        test_x, test_y = train_data.transpose()

        return test_x, train_y, test_x, test_y


















