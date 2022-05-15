from typing import List, Tuple

import socket
import select
import random
import pickle
import pygame

import Network.netlib as netlib

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080
PRINT_DEBUG = True


class Server:

    def __init__(self):

        self.IP = SERVER_IP
        self.PORT = SERVER_PORT

        # Queue of messages that server needs to send to connected clients
        self.messages_to_send = []

        self.socket = None

    def initialize(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.IP, self.PORT))
        self.socket.listen()

        if PRINT_DEBUG:
            print("Server Starting!")

    @staticmethod
    def receive_message(conn: socket.socket):
        message = conn.recv(netlib.MAX_MSG_LENGTH).decode()
        code, data = netlib.unpack_message(message)

        if PRINT_DEBUG:
            print(f"[Client {conn.getpeername()}]: {message}")

        return code, data

    def append_message(self, conn: socket.socket, code: str, data: str):

        message = netlib.pack_message(code, data)
        self.messages_to_send.append((conn, message))

        if PRINT_DEBUG:
            print(f"[Server]: {message}")

    def send_messages(self, ready_to_write: List[Tuple[socket.socket, str]]):

        # try to send all messages
        for packed_message in self.messages_to_send:
            conn, message = packed_message
            if conn in ready_to_write:
                conn.send(message.encode())
                self.messages_to_send.remove(packed_message)


    def handle_client_request_object(self, conn, data):

        amount, objects_list = netlib.split_data(data, 2)

        objects = netlib.split_data(objects_list, int(amount), data_delimiter=',')
        random_object = random.choice(objects)

        self.append_message(conn, netlib.SERVER_PROTOCOL['send_object'], random_object)

    def handle_client_message(self, conn, code, data):

        if code == netlib.CLIENT_PROTOCOL['request_object']:
            self.handle_client_request_object(conn, data)

    def run(self):
        self.initialize()

        client_sockets = []

        running = True
        # Implement code ...
        while running:
            ready_to_read, ready_to_write, in_error = select.select([self.socket] + client_sockets, client_sockets, [])

            for conn in ready_to_read:

                # self.socket will be ready to read only when a new client is trying to connect
                if conn is self.socket:
                    client_socket, address = self.socket.accept()
                    client_sockets.append(client_socket)

                    if PRINT_DEBUG:
                        print("New Client Joined")

                # clients connection will be ready to read when a client has sent a message
                else:
                    try:
                        code, data = self.receive_message(conn)

                        # add to message_to_send
                        self.handle_client_message(conn, code, data)

                    # if client crashed
                    except Exception as e:
                        print(str(e))
                        #handle_logout_message(conn)

            self.send_messages(ready_to_write)



if __name__ == '__main__':
    server = Server()
    server.run()





