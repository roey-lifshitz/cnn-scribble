import random
import struct
from struct import unpack


amount_per_drawing = 500
percent = 0.8
filenames = [
    'arm.bin',
    'anvil.bin'
]


def unpack_drawing(file_handle):

    key_id, = unpack('Q', file_handle.read(8))
    country_code, = unpack('2s', file_handle.read(2))
    recognized, = unpack('b', file_handle.read(1))
    timestamp, = unpack('I', file_handle.read(4))
    n_strokes, = unpack('H', file_handle.read(2))
    image = []
    # Loop through all strokes
    for i in range(n_strokes):
        # Unpack each stroke
        n_points, = unpack('H', file_handle.read(2))
        fmt = str(n_points) + 'B'
        x = unpack(fmt, file_handle.read(n_points))
        y = unpack(fmt, file_handle.read(n_points))
        # Add stroke to data
        image.append((x, y))

    return {
        'key_id': key_id,
        'country_code': country_code,
        'recognized': recognized,
        'timestamp': timestamp,
        'image': image
    }


def load(file_handle, amount):

    with open("data/{0}".format(file_handle), 'rb') as f:

        drawings = []
        while amount >= 0:
            # Loop until self.unpack_drawing(f) throws an error or reached amount
            try:
                drawing = unpack_drawing(f)

                if drawing['recognized']:
                    amount = amount - 1
                    drawings.append(drawing)

            except struct.error:
                print(struct.error)
                return None

        return drawings

    return None



class Data:

    def __init__(self):

        self.filenames = filenames
        self.test = []
        self.training = []

    def load(self):

        for file in filenames:
            drawings = load(file, amount_per_drawing)
            border = int(len(drawings) * percent)
            # Split data: 80% training, 20% testing
            self.training += drawings[:border]
            self.test += drawings[border + 1:]
        print(len(self.training), len(self.test))

    def shuffle(self):
        random.shuffle(self.test)
        random.shuffle(self.training)
