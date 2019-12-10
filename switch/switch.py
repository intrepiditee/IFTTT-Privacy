from flask import Flask, request, Response
from rule import Condition, Rule
from decrypt import decrypt
import time
import requests
import json
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/usr/src/app/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

RULES = {}


@app.route("/update", methods=['POST'])
def handle_update():
    if 'file' not in request.files:
        return Response(json.dumps({'error': 'missing file'}), status=400)

    files = request.files.getlist('file')
    print(files)

    for file in files:
        if file.filename == '':
            return Response(json.dumps({'error': 'missing file'}), status=400)

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    names = sorted([file.filename for file in files])
    key = "-".join(names)

    data = {}
    for name in names:
        data[name] = decrypt(name)
        print(name, data[name])

    rule = RULES[key]
    if rule.evaluate(data):
        print("State changed to " + str(rule.get_output()))
    else:
        print("State did not change.")

    return Response(status=200)


@app.route("/rule", methods=['POST'])
def handle_rules():
    rules = request.get_json()
    try:
        add_rules(rules)
    except KeyError:
        return Response(json.dumps({'error': 'missing fields'}), status=400)
    finally:
        return Response(status=200)


def add_rules(rules):
    global RULES

    rules = rules['rules']
    for rule in rules:
        conditions = []

        for condition in rule['conditions']:
            name = condition['name']
            operand = condition['operand']
            value = condition['value']

            conditions.append(Condition(name, operand, value))

        names = [condition['name'] for condition in rule['conditions']]
        key = "-".join(names)
        RULES[key] = Rule(rule['output'], conditions)


def configure(config):
    with open("phone_to_switch.json") as f:
        rules = json.load(f)
        add_rules(rules)


def get_config():
    while True:
        try:
            response = requests.get('http://ifttt_server_1:8080/configure/switch')

            config = json.loads(response.text)
            if response.status_code == 200:
                return config
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)

def main():

    config = get_config()
    name = config['name']
    add_rules(config)

    print(RULES)

    app.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
