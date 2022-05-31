from UI.canvas import Canvas
from UI.button import Button
from UI.input_box import InputBox
from UI.text_box import TextBox
from UI.chat_box import ChatBox
from UI.timer import Timer
from Network.client import Client
from NeuralNetwork.model import Model
from file_parser import FileParser

import pygame
import threading
import numpy as np
import time
import sys
from enum import Enum

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 8080


class States(Enum):
    """
    Keys for each type of screen in app
    """
    MENU = 1
    GAME = 2
    FINISH = 3


class Game:
    """
    Runs the game logic of each player
    """

    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Scribble')

        self.screen = pygame.display.set_mode((1200, 800))
        self.screen.fill((122, 122, 122))

        self._logo = pygame.image.load('images/logo.png')
        self.screen.blit(self._logo, ((1200 - 338) // 2, 10))

        # Game variables
        self.score = 0
        self.to_draw = None
        self.name = None
        self.running = False

        # Helper Classes
        self.client = Client(SERVER_IP, SERVER_PORT)
        self.file_parser = FileParser()
        self.cnn = Model(None, None, None, None)
        self.cnn.update("NeuralNetwork/Models/10_85.pkl")

        self.canvas = Canvas((100, 150, 650, 500), self.screen)

        # Dictionary of ui elements for each screen
        self.ui_elements = {
            States.MENU: self.get_menu_elements(),
            States.GAME: self.get_game_elements(),
            States.FINISH: self.get_finish_elements(),
        }

        self.clock = pygame.time.Clock()
        self.clock.tick(60)

        self.state = States.MENU

    def get_menu_elements(self):
        return {
            'title': TextBox((550, 200, 100, 40), text="Login", font_size=72, has_border=False,
                             color=(122, 122, 122)),
            'subtitle': TextBox((550, 300, 100, 40), text="Enter username:", has_border=False,
                                color=(122, 122, 122)),
            'username': InputBox((500, 380, 200, 40))
        }

    def get_game_elements(self):
        return {

            'clear_canvas': Button((800, 610, 100, 40), image=pygame.image.load("images/eraser.png"),
                                   color=(235, 232, 232), hover_color=(196, 191, 191),
                                   on_click=lambda: self.canvas.show(self.screen)),
            'post_chat': InputBox((800, 500, 300, 40)),
            'game_timer': Timer((1000, 610, 100, 40), '00h:01m:5s', color=(125, 125, 125),
                                text_color=(100, 255, 100), border_width=0),
            'chat_display': ChatBox((800, 175, 300, 300), 8),
            'object_display': TextBox((800, 560, 120, 40), text_color=(122, 255, 100)),
            'scoreboard': TextBox((980, 560, 120, 40), text=f"Score: {self.score}", text_color=(122, 255, 100))
        }

    def get_finish_elements(self):
        return {
            'title': TextBox((200, 200, 100, 40), text="Highscore", font_size=72, has_border=False,
                             color=(122, 122, 122)),
            'subtitle': TextBox((200, 300, 100, 40), text="The best player's score:", has_border=False,
                                color=(122, 122, 122)),
            'new_game': Button((1000, 610, 100, 40), text="New Game",
                               color=(235, 232, 232), hover_color=(196, 191, 191),
                               on_click=lambda *args: None),
            'score_display': ChatBox((550, 175, 300, 300), 15)
        }

    def clear_screen(self) -> None:
        """
        Draws the bg color of the screen and game logo
        :return: None
        """
        self.screen.fill((122, 122, 122))
        self.screen.blit(self._logo, ((1200 - 338) // 2, 10))

    def update_text_box(self, state: States, description: str, text: str) -> None:
        """
        Updates the text of a TextBox
        :param state: States enum
        :param description: description of element
        :param text: new text
        :return: None
        """
        if isinstance(self.ui_elements[state][description], TextBox):
            self.ui_elements[state][description].text = text
        else:
            raise TypeError(self.ui_elements[state][description])

    def predict(self) -> None:
        """
        Predicts the drawing on the canvas using the Games cnn
        :return: None
        """
        while self.running:
            if self.state == States.GAME:
                # check chat updates
                self.client.update_chat(self.ui_elements[self.state]['chat_display'])
                if pygame.mouse.get_pressed()[0]:
                    time.sleep(0.5)
                else:
                    image = self.canvas.capture()

                    if image is not None:
                        output = self.cnn.predict(image)
                        prediction = self.cnn.objects[np.argmax(output)]

                        if prediction == self.to_draw:
                            self.canvas.show(self.screen)
                            self.to_draw = self.client.request_object(self.cnn.objects)
                            self.score += 1
                            self.update_text_box(States.GAME, 'object_display', self.to_draw)
                            self.update_text_box(States.GAME, 'scoreboard', f"Score: {self.score}")

            time.sleep(0.2)


    def run(self) -> None:
        """
        Application Logic
        :return: None
        """
        self.state = States.MENU
        self.running = True
        self.client.connect()

        predict = threading.Thread(target=self.predict)
        predict.start()

        while self.running:
            dt = self.clock.tick()
            # Menu screen logic
            if self.state == States.MENU:
                # Loop for all events
                for event in pygame.event.get():
                    # Loop for all ui elements in menu screen
                    for description, element in self.ui_elements[self.state].items():
                        # handle each element events
                        if isinstance(element, InputBox):
                            text = element.handle_event(event)
                            if text:
                                if description == 'username':
                                    success = self.client.login(text)
                                    if success:
                                        # Moving into Game State
                                        self.name = text

                                        self.ui_elements[States.GAME] = self.get_game_elements()
                                        self.score = 0
                                        self.update_text_box(States.GAME, 'scoreboard', f"Score: {self.score}")
                                        self.clear_screen()
                                        self.canvas.show(self.screen)
                                        self.to_draw = None
                                        self.state = States.GAME
                                    else:
                                        self.clear_screen()
                                        self.update_text_box(States.MENU, 'subtitle', 'A player with this username is '
                                                                                      'currently online. Try Again!')
                        else:
                            element.handle_event(event)
                    if event.type == pygame.QUIT:
                        self.running = False

            # Game screen logic
            elif self.state == States.GAME:
                # Get object for the first time
                if self.to_draw is None:
                    self.to_draw = self.client.request_object(self.cnn.objects)
                    self.update_text_box(self.state, 'object_display', self.to_draw)

                # Loop for all events
                for event in pygame.event.get():
                    self.canvas.handle_event(event)
                    # Loop for all ui elements in game screen
                    for description, element in self.ui_elements[self.state].items():
                        # handle each element events
                        if isinstance(element, InputBox):
                            text = element.handle_event(event)
                            if text and description == 'post_chat':
                                self.client.send_chat(f'{self.name}: {text}')
                        elif isinstance(element, Timer):
                            finished = element.handle_event(event)
                            if finished:
                                # Moving into finish state
                                self.state = States.FINISH
                                self.clear_screen()
                                self.client.prepare_leaderboard(self.ui_elements[States.FINISH]['score_display'], self.score)
                        else:
                            element.handle_event(event)
                    if event.type == pygame.QUIT:
                        self.running = False

            # Finish screen logic
            elif self.state == States.FINISH:
                # Loop for all events
                for event in pygame.event.get():
                    # Loop for all ui elements in menu screen
                    for description, element in self.ui_elements[self.state].items():
                        # handle each element events
                        if isinstance(element, Button):
                            new_game = element.handle_event(event)
                            if new_game:
                                if description == 'new_game':
                                    # Moving into Game State
                                    self.ui_elements[States.GAME] = self.get_game_elements()
                                    self.score = 0
                                    self.update_text_box(States.GAME, 'scoreboard', f"Score: {self.score}")
                                    self.canvas.show(self.screen)
                                    self.to_draw = None
                                    self.state = States.GAME
                                    self.clear_screen()

                        else:
                            element.handle_event(event)
                    if event.type == pygame.QUIT:
                        self.running = False

            for element in self.ui_elements[self.state].values():
                element.draw(self.screen, dt)

            pygame.display.flip()

        predict.join()
        self.client.logout()

if __name__ == '__main__':
    game = Game()
    game.run()
