# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
    The following code has been modified so it could fit with our project
"""


import struct
from struct import unpack


class BinaryFileParser:

    # Unpack Data of a given file
    def unpack_drawing(self, file_handle):
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


    def unpack_drawings(self, filename):
        with open(filename, 'rb') as f:
            while True:
                try:
                    yield self.unpack_drawing(f)
                except struct.error:
                    break


    def load(self, screen, canvas):
        for drawing in self.unpack_drawings('Data/full_binary_banana.bin'):
            # do something with the drawing
            screen.fill((255, 255, 255))
            canvas.data = drawing['image']
            canvas.draw_data(screen, 2)
            return




"""
import struct
from struct import unpack


def unpack_drawing(file_handle):
    key_id, = unpack('Q', file_handle.read(8))
    country_code, = unpack('2s', file_handle.read(2))
    recognized, = unpack('b', file_handle.read(1))
    timestamp, = unpack('I', file_handle.read(4))
    n_strokes, = unpack('H', file_handle.read(2))
    print(n_strokes)

    # Size of given image is 256 * 256
    pixels = [0] * 256 * 256

    # Loop through all strokes
    for i in range(n_strokes):
        n_points, = unpack('H', file_handle.read(2))
        fmt = str(n_points) + 'B'
        # get the indexes of each pixel that has been drawn
        x = unpack(fmt, file_handle.read(n_points))
        y = unpack(fmt, file_handle.read(n_points))
        # fill the pixels array
        for index in range(len(x)):
            pixels[x[index] * 256 + y[index]] = 1

    return {
        'key_id': key_id,
        'country_code': country_code,
        'recognized': recognized,
        'timestamp': timestamp,
        'pixels': pixels
    }

def unpack_drawings(filename):
    with open(filename, 'rb') as f:
        while True:
            try:
                yield unpack_drawing(f)
            except struct.error:
                break


def loadFiles():
    for drawing in unpack_drawings('data/full_binary_anvil.bin'):
        # do something with the drawing
        print(drawing['pixels'])
"""