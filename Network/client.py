import socket
import pygame
import threading
import time
import os
import numpy as np

import Network.netlib as netlib  # To use chatlib functions or consts, use chatlib.****

from UI.canvas import Canvas
from UI.button import Button
from UI.input_box import InputBox
from UI.timer import Timer
from NeuralNetwork.neural_network import NeuralNetwork
from file_parser import FileParser

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 8080
PRINT_DEBUG = True
os.chdir("..")

class Client:

    def __init__(self):

        self.IP = SERVER_IP
        self.PORT = SERVER_PORT

        self.run_ai = True
        self.socket = None

        self.to_draw = None
        self.score = 0

    @staticmethod
    def error():
        exit()

    def connect(self):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.IP, self.PORT))

        if PRINT_DEBUG:
            print("Connected to Server")

    def send_message(self, code, data):
        """
            Builds a new message using chatlib, wanted code and message.
            Prints debug info, then sends it to the given socket.
            Paramaters: conn (socket object), code (str), data (str)
            Returns: Nothing
        """
        message = netlib.pack_message(code, data)

        if message:
            self.socket.send(message.encode())

    def receive_message(self):

        message = self.socket.recv(1024).decode()
        code, data = netlib.unpack_message(message)
        return code, data

    def send_and_recive(self, code, data):
        self.send_message(code, data)
        return self.receive_message()

    def request_object(self, objects):

        objects_list = ",".join(objects)
        code, data = self.send_and_recive(netlib.CLIENT_PROTOCOL['request_object'], f"{len(objects)}#{objects_list}")
        if code == netlib.SERVER_PROTOCOL['send_object']:
            print(data)
            return data.split(".")[0]

    def build_app(self):
        pygame.init()
        pygame.font.init()
        background_colour = (122, 122, 122)
        screen = pygame.display.set_mode((1000, 800))

        pygame.display.set_caption('Scribble')
        screen.fill(background_colour)

        bg_pattern = pygame.image.load('Images/pattern.png')
        screen.blit(bg_pattern, (0, 0))

        logo = pygame.image.load('images/logo.png')
        screen.blit(logo, ((1000 - 338) // 2, 10))

        canvas = Canvas(screen, 150, 150, 700, 500)
        file_parser = FileParser()

        clock = pygame.time.Clock()
        clock.tick(60)

        ai = NeuralNetwork(None, None, None, file_parser.files)
        ai.load("NeuralNetwork/Models/10_75%_extra_large.pkl")

        img = pygame.image.load("images/eraser.png")
        ui_elements = [
            Button((880, 560, 100, 40), image=img, color=(235, 232, 232), hover_color=(196, 191, 191),
                   on_click=canvas.fill),
            Button((880, 610, 100, 40), text="predict",
                   on_click=lambda: print(ai.objects[np.argmax(ai.predict(canvas.capture()))])),
            InputBox((880, 510, 100, 40)),
            Timer((880, 200, 100, 40), '00h:01m:05s', color=(125, 125, 125), text_color=(100, 255, 100), border_width=0)
        ]

        return screen, canvas, clock, ui_elements, file_parser, ai

    def start_ai(self, ai, canvas):

        while self.run_ai:
            image = canvas.capture()

            if image is not None:
                output = ai.predict(image)
                prediction = ai.objects[np.argmax(output)].split(".")[0]

                if prediction == self.to_draw:
                    self.score += 1;
                    self.to_draw = self.request_object(ai.objects)

                print(prediction)

            time.sleep(1)

    def run(self):

        self.connect()

        screen, canvas, clock, ui_elements, file_parser, ai = self.build_app()

        # Start making ai predict
        thread = threading.Thread(target=self.start_ai, args=(ai, canvas))
        thread.start()

        self.to_draw = self.request_object(ai.objects)

        total_time = 0
        running = True
        while running:
            dt = clock.tick()
            for event in pygame.event.get():
                canvas.update(event)

                for element in ui_elements:
                    element.handle_event(event)

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:

                        new_object = self.request_object(ai.objects)
                        while new_object == self.to_draw:
                            new_object = self.request_object()
                            
                        self.to_draw = new_object


            for element in ui_elements:
                element.draw(screen, dt)

            pygame.display.flip()
            total_time += dt


if __name__ == '__main__':
    client = Client()
    client.run()
