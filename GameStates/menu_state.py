from GameStates.base import GameState, State
from UI.button import Button

from typing import Optional, Tuple, Dict

import warnings
import pygame


class MenuState(GameState):

    def __init__(self, screen):
        self.screen = screen
        self.state = State.menu

        self.ai_button = Button((100, 100, 400, 400),
                                "AI",
                                on_click= lambda: self.update_state(State.ai))

        self.multiplayer_button = Button((500, 100, 400, 400),
                                         "Multiplayer",
                                         on_click=lambda: self.update_state(State.multiplayer))


    def update_state(self, state):
        self.state = state
        print(state)


    def render(self):
        self.ai_button.draw(self.screen)
        self.multiplayer_button.draw(self.screen)

    def run(self):

        for event in pygame.event.get():

            self.ai_button.handle_event(event)
            self.multiplayer_button.handle_event(event)

        self.render()




