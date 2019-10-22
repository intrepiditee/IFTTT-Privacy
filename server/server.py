from flask import Flask, request
import requests
from collections import defaultdict, deque
from homomorphic_computations import *
import json

data_cache = defaultdict(lambda: deque([0] * 100, 100))

class DataCache():
    def __init__(self, max_items):
        self.data = defaultdict(lambda: deque([0] * 100, 100))

    def add_value(self, name, value):
        self.data[name].append(value)

    def has_value(self, name):
        return name in self.data

    def get_range(self, name, num_values):
        return self.data[name][-num_values:]

    def get_value(self, name):
        return self.data[name]

class Computation():
    def __init__(self, config):
        self.computation_type = config["type"]
        if config["type"] == "ident":
            self.datapoints = [[config["datapoint"]]]
            self.name = config["datapoint"]
        elif config["type"] == "rate" or config["type"] == "run_sum":
            self.num = config["num"]
            self.datapoints = [[config["datapoint"]]]
        else:
            self.datapoints = config["datapoints"]
            self.name = config["name"]
        self.output = config["output"]

    def compute(self, data_cache):
        if self.computation_type == "ident":
            return data_cache.get_value(self.datapoints[0])
        elif self.computation_type == "+":
            result = data_cache.get_value(self.datapoints[0])
            for i in range(1, len(self.datapoints)):
                result = h_sum(result, data_cache.get_value(self.datapoints[0]))
            return result
        elif self.computation_type == "*":
            result = data_cache.get_value(self.datapoints[0])
            for i in range(1, len(self.datapoints)):
                result = h_prod(result, data_cache.get_value(self.datapoints[0]))
            return result
        elif config["type"] == "rate":
            data = data_cache.get_range(self.datapoints[0], self.num)
            result = h_diff(data[1], data[0])
            for i in range(1, len(data) - 1):
                result = h_sum(result, h_diff(data[i+1, data[i]]))
            return result
        elif config["type"] == "run_sum":
            data = data_cache.get_range(self.datapoints[0], self.num)
            result = data[0]
            for i in range(1, len(data)):
                result = h_sum(result, data[i])
            return result

    def __str__(self):
        return self.computation_type + "(" + ",".join(self.datapoints) + ")" + ("" if self.computation_type != "rate" and self.computation_type != "run_sum" else "(" + str(self.num) + ")")"->" + self.output

class Server():
    def __init__(self, config):
        self.sensor_to_computations = defaultdict(set)
        self.switch_to_datapoints = defaultdict(set)
        self.computations = [Computation(computation_config) for computation_config in config["computations"]]
        for computation_config in config["computations"]:
            for switch in computation_config["output"]:
                if "name" in computation_config:
                    self.switch_to_datapoints[switch].add(computation_config["name"])
                else:
                    self.switch_to_datapoints[switch].add(computation_config["datapoint"])
        for computation in computations:
            for datapoint in computation.datapoints:
                self.sensor_to_computations[datapoint].add(computation)
        self.data_cache = DataCache(100)
        self.switch_to_address = {}
        for switch in config["switches"]:
            self.switch_to_address[switch["name"]] = switch["address"]

    def update_switch(self, switch):
        data = {datapoint: self.data_cache.get_value(datapoint) for datapoint in self.switch_to_datapoints[switch]}
        requests.post(self.switch_to_address[switch], data=data)

    def process_data(self, sensor, value):
        self.data_cache.add_value(sensor, value)
        affected_switches = set([])
        for computation in self.sensor_to_computations[sensor]:
            self.data_cache.add_value(computation.output, computation.compute(self.data_cache))
            for switch in computation.output:
                affected_switches.add(switch)
        for switch in affected_switches:
            self.update_switch(switch)

def load_config():
    data = json.load("phone_config.json")
    return data

server = Server(load_config())

app = Flask(__name__)
@app.route("/upload", methods=['POST'])
def handle_upload():
    data = request.form['data']
    server.process_data(data["sensor"], data["value"])
    return "Recieved"

@app.route("/")
def hello():
    return "I am the server!"

def main():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
