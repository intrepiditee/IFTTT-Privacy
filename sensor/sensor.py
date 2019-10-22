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


def main():
    filename = 'ifttt_sensor_1'
    while True:
        data = random.randrange(60, 80)
        encrypt(data, filename)
        files = [('file', open(filename, 'rb'))]
        requests.post("http://ifttt_server_1:8080/upload", files=files)
        time.sleep(2)

    # app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
    
