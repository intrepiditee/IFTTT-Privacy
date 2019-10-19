from flask import Flask, request

app = Flask(__name__)

EXPECTED = {}

@app.route("/report", methods=['POST'])
def handle_report():
    switch = request.form['switch']
    status = request.form['status']

    if EXPECTED[switch] != status:
        print(f'Error: {switch} got {status}!')

    return "Recieved"



@app.route("/")
def hello():
    return "I am the receiver!"


def read_expected_results():
    global EXPECTED

    with open('tests.tsv', "rt") as f:
        next(f)
        for line in f:
            fields = line.split()
            switch = fields[2]
            status = fields[3]
            EXPECTED[switch] = status


def main():
    read_expected_results()
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
    
