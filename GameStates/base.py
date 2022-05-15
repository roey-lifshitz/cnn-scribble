from abc import ABC, abstractmethod
from enum import Enum


class State(Enum):
    menu = 1
    ai = 2
    multiplayer = 3


class GameState(ABC):

    def __init__(self, app):
        self.app = app
        self.state = None
        self.prev_state = None



    @abstractmethod
    def run(self):
        pass

