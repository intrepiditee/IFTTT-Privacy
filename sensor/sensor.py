from flask import Flask, request
import requests

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
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
    
