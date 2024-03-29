from encrypt import encrypt
import requests
import random
import time
import json


def get_config():
    while True:
        try:
            response = requests.get('http://ifttt_server_1:8080/configure/sensor')

            config = json.loads(response.text)
            if response.status_code == 200:
                return config
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)


def main():
    config = get_config()

    min = config["min"]
    max = config["max"]
    interval = config["interval"]
    name = config["name"]

    while True:
        data = random.randrange(min, max)
        encrypt(data, name)
        files = [('file', open(name, 'rb'))]

        try:
            resp = requests.post("http://ifttt_server_1:8080/upload", files=files)
            if resp.status_code != 200:
                print("Server returned code " + str(resp.status_code))
        except requests.exceptions.ConnectionError:
            print("Failed to post to server")

        print("Post!")
        time.sleep(interval)


if __name__ == "__main__":
    main()
