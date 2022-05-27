import socket
import Network.netlib as netlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 8080
PRINT_DEBUG = True


class Client:

    def __init__(self, ip, port):

        self.IP = SERVER_IP
        self.PORT = SERVER_PORT

        self.socket = None

        self.name = ""
        self.to_draw = None
        self.score = 0

    @staticmethod
    def error():
        print("Client Error")
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

    def send_and_receive(self, code, data):
        self.send_message(code, data)
        return self.receive_message()

    def login(self, username):
        code, data = self.send_and_receive(netlib.CLIENT_PROTOCOL["request_login"], f"{username}")

        if code == netlib.SERVER_PROTOCOL["login_success"]:
            self.name = username
            return True
        else:
            if PRINT_DEBUG:
                print(f"Failed Login {data}! Try Again.\n")
            return False

    def logout(self):
        self.send_message(netlib.CLIENT_PROTOCOL['request_logout'], "")

    def request_object(self, objects):

        objects_list = ",".join(objects)

        code, data = self.send_and_receive(netlib.CLIENT_PROTOCOL['request_object'], f"{len(objects)}#{objects_list}")

        if code == netlib.SERVER_PROTOCOL['send_object']:

            while data == self.to_draw:
                code, data = self.send_and_receive(netlib.CLIENT_PROTOCOL['request_object'],
                                                   f"{len(objects)}#{objects_list}")

                if code != netlib.SERVER_PROTOCOL['send_object']:
                    self.error()
        return data

    def prepare_leaderboard(self, leaderboard, score):
        code, data = self.send_and_receive(netlib.CLIENT_PROTOCOL["update_score"], f"{self.name}#{score}")

        if code != netlib.SERVER_PROTOCOL["score_received"]:
            self.error()

        leaderboard.clear()
        highscores = netlib.split_data(data, -1)
        for highscore in highscores[:leaderboard.amount]:
            leaderboard.append_text(highscore)

    def send_chat(self, text):
        code, data = self.send_and_receive(netlib.CLIENT_PROTOCOL["update_chat"], f"{text}")

        if code != netlib.SERVER_PROTOCOL["chat_received"]:
            print("ERROR SEND CHAT")
            self.error()

    def update_chat(self, chat_box):
        code, data = self.send_and_receive(netlib.CLIENT_PROTOCOL["request_chat"], "")

        if code != netlib.SERVER_PROTOCOL["send_chat"]:
            print("error in return 2")
            self.error()

        if data != "":
            messages = netlib.split_data(data, -1)
            for message in messages[1:]:
                chat_box.append_text(message)


