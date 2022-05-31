from typing import List, Tuple

import socket
import select
import random

import Network.netlib as netlib

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080
PRINT_DEBUG = True


class Server:

    def __init__(self):

        self.IP = SERVER_IP
        self.PORT = SERVER_PORT

        # List of all connected sockets
        self.client_sockets = []
        # Queue of messages that server needs to send to connected clients
        self.messages_to_send = []

        # Dictionary of connected socket to username
        self.players = {}
        # list of tuple (username: score)
        self.leaderboards = []

        with open('leaderboard.txt', 'r') as f:
            for line in f:
                print(line)
                name, score = netlib.split_data(line, 2, ":")
                self.leaderboards.append((name, int(score)))
        # Queue of all chat messages each socket needs to receive
        self.chat_queue = {}

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
            if code != netlib.CLIENT_PROTOCOL['update_chat'] and message == "":
                print(f"[Client {conn.getpeername()}]: {message}")

        return code, data

    def append_message(self, conn: socket.socket, code: str, data: str):

        message = netlib.pack_message(code, data)
        self.messages_to_send.append((conn, message))

        if PRINT_DEBUG:
            if code == netlib.SERVER_PROTOCOL['send_chat'] and message == "SEND_CHAT       |0000|":
                return
            print(f"[Server]: {message}")

    def send_messages(self, ready_to_write: List[Tuple[socket.socket, str]]):

        # try to send all messages
        for packed_message in self.messages_to_send:
            conn, message = packed_message
            if conn in ready_to_write:
                conn.send(message.encode())
                self.messages_to_send.remove(packed_message)

    def handle_client_login(self, conn: socket.socket, data: str) -> None:
        """
        Handles clients login request
        :param conn: Clients socket
        :param data: Clients name
        :return: None
        """
        if data in self.players.values():
            self.append_message(conn, netlib.SERVER_PROTOCOL["login_failed_dup_id"], "DUP_ID")
        else:
            # Add client to player dictionary: socket: username
            self.players.update({conn: data})
            # Add client message queue: socket: chat_messages
            self.chat_queue.update({conn: ""})
            # Add client to leaderboard: [username: score]
            self.append_message(conn, netlib.SERVER_PROTOCOL["login_success"], "")

    def handle_client_logout(self, conn: socket.socket) -> None:
        """
        Handles clients logout request
        :param conn: Clients socket
        :return:
        """
        # Delete from dictionary
        self.chat_queue.pop(conn, None)
        self.players.pop(conn, None)
        self.client_sockets.remove(conn)
        print(f"{conn.getpeername()} Disconnected")
        conn.close()

    def handle_client_request_object(self, conn: socket.socket, data: str) -> None:
        """
        Handles clients object request, sends a random object to the client
        :param conn: Clients socket
        :param data: str: "amount_of_objects|object_a,object_b,object_c"
        :return: None
        """
        # Unpack data
        amount, objects_list = netlib.split_data(data, 2)
        objects = netlib.split_data(objects_list, int(amount), data_delimiter=',')
        # Send random object
        random_object = random.choice(objects)
        self.append_message(conn, netlib.SERVER_PROTOCOL["send_object"], random_object)

    def handle_client_update_score(self, conn: socket.socket, data: str) -> None:
        """
        Handles client score
        :param conn: Clients socket
        :param data: score
        :return: None
        """
        name, score = netlib.split_data(data, 2)

        with open('leaderboard.txt', 'at') as f:
            f.write(f"\n{name}:{score}")

        self.leaderboards.append((name, int(score)))
        # sort leaderboards
        self.leaderboards = sorted(self.leaderboards, key=lambda v: v[1], reverse=True)[:15]

        score = ['%s: %s' % t for t in self.leaderboards]
        score = '#'.join(score)

        self.append_message(conn, netlib.SERVER_PROTOCOL["score_received"], score)

    def handle_client_update_chat(self, conn: socket.socket, data: str) -> None:
        """
        Handles clients chat message, adds the message to the message dictionary queue
        :param conn: Clients socket
        :param data: message
        :return: None
        """
        for client_socket in self.client_sockets:
            if client_socket in self.chat_queue.keys():
                self.chat_queue[client_socket] += f"#{data}"

        self.append_message(conn, netlib.SERVER_PROTOCOL["chat_received"], "")

    def handle_client_receive_chat(self, conn):
        """
        Handles client message request, sends all messages in the chat queue for the client
        :param conn: Clients socket
        :return:
        """
        self.append_message(conn, netlib.SERVER_PROTOCOL["send_chat"], self.chat_queue[conn])
        self.chat_queue[conn] = ""


    def handle_client_message(self, conn: socket.socket, code: str, data: str) -> None:
        """
        Calls the correct handle function according the given code by client
        :param conn: Clients socket
        :param code: Protocol code
        :param data: Protocol Data
        :return: None
        """
        if code == netlib.CLIENT_PROTOCOL["request_login"]:
            self.handle_client_login(conn, data)
        elif code == netlib.CLIENT_PROTOCOL["request_logout"]:
            self.handle_client_logout(conn)
        elif code == netlib.CLIENT_PROTOCOL["request_object"]:
            self.handle_client_request_object(conn, data)
        elif code == netlib.CLIENT_PROTOCOL["update_score"]:
            self.handle_client_update_score(conn, data)
        elif code == netlib.CLIENT_PROTOCOL["update_chat"]:
            self.handle_client_update_chat(conn, data)
        elif code == netlib.CLIENT_PROTOCOL["request_chat"]:
            self.handle_client_receive_chat(conn)


    def run(self) -> None:
        """
        Server Running Loop
        Communicates with all connected clients
        Connects with new clients
        :return: None
        """
        # Start socket
        self.initialize()

        running = True
        while running:

            # ready_to_read- all sockets we can read messages from
            # ready_to_write- all sockets we can write messages to
            # in_error- all sockets that had an error
            ready_to_read, ready_to_write, in_error = select.select([self.socket] + self.client_sockets,
                                                                    self.client_sockets,
                                                                    [])
            # Loop through all the sockets that sent a message
            for conn in ready_to_read:
                # self.socket will be ready to read only when a new client is trying to connect
                if conn is self.socket:
                    # add socket that has connected to client socket list
                    client_socket, address = self.socket.accept()
                    self.client_sockets.append(client_socket)

                    if PRINT_DEBUG:
                        print("New Client Joined")

                # clients connection will be ready to read when a client has sent a message
                else:
                    try:
                        code, data = self.receive_message(conn)
                        # handle a the received message and send a response accordingly
                        self.handle_client_message(conn, code, data)

                    # if client crashed
                    except Exception as e:
                        print(e)
                        self.handle_client_logout(conn)

            # send all messages in the message queue
            self.send_messages(ready_to_write)


if __name__ == '__main__':
    server = Server()
    server.run()
