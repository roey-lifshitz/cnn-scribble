from typing import Tuple, List
import warnings
import numpy as np


class FileParser:
    """
    FilParser: Parses .npy files from googles QuickDraws data set
    https://github.com/googlecreativelab/quickdraw-dataset
    """

    def __init__(self) -> None:

        self.files = [
            'apple.npy',
            'duck.npy',
            'foot.npy',
            'sun.npy'
        ]

    def clear(self) -> None:
        """
        Clears all files in self.files
        :return: None
        """
        self.files.clear()

    def update(self, files: List[str]) -> None:
        """
        Update the files that self.load() is going to load drawings from
        :param files: List of new files to add
        :return:
        """
        # Loop through new files
        for file in files:
            # Check that is a .npy file
            extension = file.split(".")[-1]
            if extension != ".npy":
                warnings.warn(f"{file} excluded! file extension is .{extension} instead of .npy!")
                continue
            # Check that does not already exist
            if file not in self.files:
                self.files.append(file)

    def load(self, train_amount: int = 300, test_amount: int = 50, seed: int = 99) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Returns training and test data sets
        :param train_amount: Total amount of training data to parse
        :param test_amount: Total amount of test data to parse
        :param seed: for randomizing array
        :return: Tuple[train_x, train_y, test_x, test_y]
        """
        # Cannot load less than one drawing per file
        if 0 < test_amount < len(self.files) or 0 < train_amount < len(self.files):

            raise ValueError("amount is smaller than files in Class, Cannot load less than one file per file")

        # Cannot load from zero files
        if not len(self.files):
            raise ValueError(f"self.files is currently Empty, Wont load anything!")

        np.random.seed(seed)

        # Prepare variables for loading
        amount_of_files = len(self.files)
        train_amount_per_file = train_amount // amount_of_files
        test_amount_per_file = test_amount // amount_of_files
        offset = train_amount_per_file

        # numpy arrays with 2 columns: 1. 1X28X28 pixels of image, 2. Vector of corresponding output
        train_data = np.empty((train_amount, 2), dtype=object)
        test_data = np.empty((test_amount, 2), dtype=object)

        # Loop through all files
        for i, file in enumerate(self.files):

            # Load images from .npy file
            images = np.load(f"data/{file}") / 255.
            # Reshape that each image will be in a 1X28X28 format
            images = images.reshape(-1, 1, 28, 28, 1)

            # binary array that represents the location of the file in self.files
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


















