import socket
import struct
import time


class Listener:
    def __init__(self, server_ip: str, server_port: int) -> None:
        self._cmd_raw: int = 10
        self._cmd: bytes = self._cmd_raw.to_bytes()

        self._server_ip: str = server_ip
        self._server_port: int = server_port

        self.client_socket: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )

    def start(self, func) -> None:
        try:
            while True:
                self.client_socket.connect((self._server_ip, self._server_port))

                while self.client_socket.sendall(self._cmd) == False:
                    message: bytes = self.client_socket.recv(12)

                    numTrialCount, numTrialCountTrue, correct_rate = struct.unpack(
                        "<iif", message
                    )

                    func(numTrialCount, numTrialCountTrue, correct_rate)
                    self.client_socket.shutdown()

                    time.sleep(1)

        except Exception as e:
            print(f"error occured: {e}")

        finally:
            self.start(func)

    def close(self):
        self.client_socket.close()
