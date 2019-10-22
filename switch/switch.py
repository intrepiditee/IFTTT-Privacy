from flask import Flask, request, Response
import requests
import json

app = Flask(__name__)

RULES = {}

@app.route("/update", methods=['POST'])
def handle_update():
    update = request.get_json()
    if 'rule_id' not in update:
        return Response(json.dumps({'error': 'missing rule_id field'}), status=400)

    if 'data' not in update:
        return Response(json.dumps({'error': 'missing data field'}), status=400)

    idd = update['rule_id']
    if idd not in RULES:
        return Response(json.dumps({'error': 'rule_id not recognized'}), status=400)

    rule = RULES[idd]    
    if rule.evaluate(update['data']):
        print("State changed to " + str(rule.output()))    

    return Response(status=200)


class Condition:

    def __init__(self, name, operand, value):
        '''
        Parameters
        ----------
        name: str
            name of the condition
        operand: str
            one of =, <, >
        value:
            threshold constant
        '''
        self.name = name
        self.operand = operand
        self.value = value

    def evaluate(self, data):
        '''
        Parameters
        ----------
        data: int
            data to be evaluated against this condition
        
        Returns
        -------
        bool
            whether this condition evaluates to true
        '''
        if self.operand == '=':
            return data == self.value;
        elif self.operand == '>':
            return data > self.value;
        elif self.operand == '<':
            return data < self.value;
        else:
            return False


class Rule:

    def __init__(self, output, conditions):
        '''
        Parameters
        ----------
        output: int
            the value to output if this rule evaluates to true
        conditions: list
            list of conditions
        '''
        self.output = output
        self.conditions = {}
        for condition in conditions:
            self.conditions[condition.name] = condition

    def evaluate(self, data):
        '''
        Parameters
        ----------
        data: dict
            dictionary from condition name to data for the condition to evaluate

        Returns
        -------
        bool
            whether all conditions evaluate to true
        '''
        for condition in self.conditions:
            if condition.name not in data:
                return False

            if not condition.evaluate(data[condition.name]):
                return False

        return True

    def output(self):
        '''
        Returns
        -------
        int
            the value to output if this rule evaluates to true
        '''
        return self.output



@app.route("/rule", methods=['POST'])
def add_rule():
    return "added"

@app.route("/")
def hello():
    return "I am a switch!"


def read_rules():
    global RULES

    with open("phone_to_switch.json") as f:
        rules = json.load(f)
    
    rules = rules['rules']
    for rule in rules:
        conditions = []
        for condition in rule['conditions']:
            name = condition['name']
            operand = condition['operand']
            value = condition['value']

            conditions.append(Condition(name, operand, value))

        RULES[rule['rule_id']] = Rule(rule['output'], conditions)

    
def main():
    read_rules();
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
    