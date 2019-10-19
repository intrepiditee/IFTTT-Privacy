from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/update", methods=['POST'])
def handle_update():
    data = request.form['data']
    print("Received " + data + "!")
    requests.post("http://ifttt_tester_1:8080/report", data={"switch": 1, "status": data})
    print("Sent " + data + "!")
    return "Recieved"

@app.route("/")
def hello():
    return "I am a switch!"

def main():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
    