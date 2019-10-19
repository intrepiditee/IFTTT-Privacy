from flask import Flask, request
import requests

app = Flask(__name__)
@app.route("/upload", methods=['POST'])
def handle_upload():
    data = request.form['data']
    print("Received " + data + "!")
    requests.post("http://ifttt_switch_1:8080/update", data={"data": data})
    print("Sent " + data + "!")
    return "Recieved"


@app.route("/")
def hello():
    return "I am the server!"

def main():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
    
