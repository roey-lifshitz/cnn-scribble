from UI.canvas import Canvas
from UI.button import Button
from UI.input_box import InputBox
from UI.text_box import TextBox
from UI.chat_box import ChatBox
from UI.timer import Timer
from NeuralNetwork.neural_network import NeuralNetwork
from file_parser import FileParser

import socket
import pygame
import threading
import time
import os
import numpy as np
import Network.netlib as netlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 8080
PRINT_DEBUG = True
os.chdir("..")

class Game:

    def __init__(self):

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Scribble')

        self.screen = pygame.display.set_mode((1200, 800))

        self.screen.fill((122, 122, 122))
        logo = pygame.image.load('images/logo.png')
        self.screen.blit(logo, ((1200 - 338) // 2, 10))

        self.canvas = Canvas(self.screen, 100, 150, 650, 500)
        self.file_parser = FileParser()
        self.ai = NeuralNetwork(None, None, None, None)
        self.ai.load("NeuralNetwork/Models/10_85.pkl")

        img = pygame.image.load("images/eraser.png")
        self.ui_elements = [
            Button((800, 610, 100, 40), image=img, color=(235, 232, 232), hover_color=(196, 191, 191),
                   on_click=self.canvas.fill),
            InputBox((800, 500, 300, 40)),
            Timer((1000, 610, 100, 40), '00h:01m:05s', color=(125, 125, 125), text_color=(100, 255, 100),
                  border_width=0)
        ]

        self.clock = pygame.time.Clock()
        self.clock.tick(60)

        self.chat_box = ChatBox((800, 175, 300, 300), 8)
        self.text_box = TextBox((800, 560, 100, 40), text_color=(122, 255, 100))
        self.scoreboard = TextBox((1000, 560, 100, 40), text_color=(100, 100, 100))
        self.scoreboard.text = f"Score: {self.score}"


    def draw(self, dt):

        for element in self.ui_elements:
            element.draw(self.screen, dt)

        self.chat_box.draw(self.screen, dt)
        self.text_box.draw(self.screen, dt)
        self.scoreboard.draw(self.screen, dt)

    def handle_ui_events(self, event):
        self.canvas.update(event)
        to_return = None

        for element in self.ui_elements:
            if isinstance(element, InputBox):
                text = element.handle_event(event)
                if text:
                    to_return = text
            else:
                element.handle_event(event)

        return to_return

    def update_object_textbox(self, text):



    def _thread(self, ai, canvas, text_box, scoreboard, chat_box):

        while self.run_ai:
            if not pygame.mouse.get_pressed()[0]:
                image = canvas.capture()

                if image is not None:
                    output = ai.predict(image)
                    prediction = ai.objects[np.argmax(output)]

                    if PRINT_DEBUG:
                        print(prediction)

                    if prediction == self.to_draw:
                        canvas.fill((255, 255, 255))

                        self.to_draw = self.request_object(ai.objects)
                        text_box.text = self.to_draw

                        self.score += 1;
                        scoreboard.text = f"Score: {self.score}"

                        self.update_score()

            time.sleep(1)
            self.update_chat(chat_box)


    def run(self):

        self.connect()
        self.login()


        screen, canvas, clock, ui_elements, file_parser, ai = build_app()

        chat_box = ChatBox((800, 175, 300, 300), 8)
        text_box = TextBox((800, 560, 100, 40), text_color=(122, 255, 100))
        scoreboard = TextBox((1000, 560, 100, 40), text_color=(100, 100, 100))
        scoreboard.text = f"Score: {self.score}"

        # Ai prediction thread
        ai_thread = threading.Thread(target=self._thread, args=(ai, canvas, text_box, scoreboard, chat_box))
        ai_thread.start()

        self.to_draw = self.request_object(ai.objects)
        text_box.text = self.to_draw

        total_time = 0
        running = True
        while running:
            dt = clock.tick()
            for event in pygame.event.get():
                canvas.update(event)

                for element in ui_elements:
                    if isinstance(element, InputBox):
                        text = element.handle_event(event)
                        if text:
                            self.send_chat(f"{self.name}: {text}")
                    else:
                        element.handle_event(event)

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:

                        canvas.fill((255, 255, 255))
                        self.to_draw = self.request_object(ai.objects)
                        text_box.text = self.to_draw

            for element in ui_elements:
                element.draw(screen, dt)

            chat_box.draw(screen, dt)
            text_box.draw(screen, dt)
            scoreboard.draw(screen, dt)

            pygame.display.flip()
            total_time += dt


if __name__ == '__main__':
    client = Client()
    client.run()
