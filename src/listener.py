import socket
import struct
import time
from turtle import listen


class Listener:
    def __init__(self, server_ip, server_port) -> None:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client_socket.connect((server_ip, server_port))

    def start(self, func) -> None:
        try:
            while True:
                print("Listening")
                message = self.client_socket.recv(12)
                print(message)
                if not message:
                    time.sleep(1)

                numTrialCount, numTrialCountTrue, correct_rate = struct.unpack(
                    "<iif", message
                )
                print(numTrialCount)

                func(numTrialCount, numTrialCountTrue, correct_rate)

        except Exception as e:
            print(f"error occured: {e}")
        finally:
            self.client_socket.close()

    def close(self):
        self.client_socket.close()
