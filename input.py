import pygame
from enum import Enum

class State(Enum):
    key_down = 0
    key_up = 1
    key_pressed = 2

    def get_state(self, key):
        # Get single even in Queue
        event = pygame.event.poll()
        if event.key == key:
            if event.type == pygame.KEYDOWN:
                return 0
            elif event.type == pygame.KEYUP:
                return 1


def default():
    return 0

class Input:

    def __init__(self):
        self.keycode = {
            "K_q" : [default, default, default],

        }

    def get_key_down(self, key, *args):
        # Get all possible functions of a key
        funcs = self.keycode.get(key)
        # Call the function given a state
        funcs[State.get_state((key))](*args)
