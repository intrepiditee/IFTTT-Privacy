from flask import Flask, request
from encrypt import encrypt
import requests
import random
import time

app = Flask(__name__)


@app.route("/send", methods=['POST'])
def handle_send():
    data = request.form['data']
    print("Received " + data + "!")
    requests.post("http://ifttt_server_1:8080/upload", data={"sensor": 1, "data": data})
    print("Sent " + data + "!")
    return "Recieved"

@app.route("/")
def hello():
    return "I am a sensor!"


def read_hostname():
    return raw_input("Enter hostname: ")

def main():
    
    hostname = read_hostname()

    while True:
        data = random.randrange(60, 80)
        encrypt(data, hostname)
        files = [('file', open(hostname, 'rb'))]
        requests.post("http://ifttt_server_1:8080/upload", files=files)
        time.sleep(5)

    # app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
    
