import json
import time
import requests


class HttpListener:
    def __init__(self) -> None:
        self.url = "http://localhost:4202/api/data"

    def stop(self):
        self.is_running = False

    def listening(self, func) -> None:
        self.is_running = True

        while self.is_running:
            try:
                response: requests.Response = requests.get(self.url)

                data: json = response.json()
                func(data)

            except Exception as e:
                print(e)

                time.sleep(5)
