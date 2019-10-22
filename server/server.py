from flask import Flask, request
import requests
from collections import defaultdict, deque
from homomorphic_computations import *
import json
import itertools

data_cache = defaultdict(lambda: deque([0] * 100, 100))

class DataCache():
    def __init__(self, max_items):
        self.data = defaultdict(lambda: deque([None] * 100, 100))
        self.max_items = max_items

    def add_value(self, name, value):
        self.data[name].append(value)

    def has_value(self, name):
        return name in self.data

    def get_range(self, name, num_values):
        return list(itertools.islice(self.data[name], self.max_items - num_values, self.max_items))

    def get_value(self, name):
        return self.data[name][-1]

class Computation():
    def __init__(self, config):
        self.computation_type = config["type"]
        if config["type"] == "ident":
            self.datapoints = [config["datapoint"]]
        elif config["type"] == "rate" or config["type"] == "run_sum":
            self.num = config["num"]
            self.datapoints = [config["datapoint"]]
        else:
            self.datapoints = config["datapoints"]
        self.name = config["name"]
        self.output = config["output"]

    def compute(self, data_cache):
        for dp in self.datapoints:
            if not self.data_cache.has_value(dp):
                return None
        if self.computation_type == "ident":
            return data_cache.get_value(self.datapoints[0])
        elif self.computation_type == "+":
            result = data_cache.get_value(self.datapoints[0])
            for i in range(1, len(self.datapoints)):
                result = h_sum(result, data_cache.get_value(self.datapoints[0]))
            return result
        elif self.computation_type == "-":
            return h_diff(data_cache.get_value(self.datapoints[0]), data_cache.get_value(self.datapoints[0]))
        elif self.computation_type == "*":
            result = data_cache.get_value(self.datapoints[0])
            for i in range(1, len(self.datapoints)):
                result = h_prod(result, data_cache.get_value(self.datapoints[0]))
            return result
        elif self.computation_type == "rate":
            data = data_cache.get_range(self.datapoints[0], self.num)
            result = h_diff(data[1], data[0])
            for i in range(1, len(data) - 1):
                result = h_sum(result, h_diff(data[i+1], data[i]))
            return result
        elif self.computation_type == "run_sum":
            data = data_cache.get_range(self.datapoints[0], self.num)
            result = data[0]
            for i in range(1, len(data)):
                result = h_sum(result, data[i])
            return result
        else:
            print("ERROR: unknown computation type", self.computation_type)

    def __str__(self):
        return self.computation_type + "(" + ",".join(self.datapoints) + ")" + ("" if self.computation_type != "rate" and self.computation_type != "run_sum" else "(" + str(self.num) + ")") + "->" + ",".join(self.output)

class Server():
    def __init__(self, config):
        self.sensor_to_computations = defaultdict(set)
        self.switch_to_datapoints = defaultdict(set)
        self.computations = [Computation(computation_config) for computation_config in config["computations"]]
        for computation_config in config["computations"]:
            for switch in computation_config["output"]:
                self.switch_to_datapoints[switch].add(computation_config["name"])
        for computation in self.computations:
            for datapoint in computation.datapoints:
                self.sensor_to_computations[datapoint].add(computation)
        self.data_cache = DataCache(100)
        self.switch_to_address = {}
        for switch in config["switches"]:
            self.switch_to_address[switch["name"]] = switch["address"]

    def update_switch(self, switch):
        print("Updating switch", switch, "w/ data", ",".join(self.switch_to_datapoints[switch]))
        for dp in self.switch_to_datapoints[switch]:
            if not self.data_cache.has_value(dp):
                print("ERROR: failed sending to switch", switch, ", not enough data")
        files = [('file', open(self.data_cache.get_value(datapoint), 'rb')) for datapoint in self.switch_to_datapoints[switch]]
        requests.post(self.switch_to_address[switch], files=files)

    def process_data(self, sensor, value):
        self.data_cache.add_value(sensor, value)
        affected_switches = set([])
        for computation in self.sensor_to_computations[sensor]:
            result = computation.compute(self.data_cache)
            if result:
                self.data_cache.add_value(computation.name, computation.compute(self.data_cache))
                for switch in computation.output:
                    affected_switches.add(switch)
            else:
                print("ERROR: failed computing computation", str(computation), ", not enough data")

        for switch in affected_switches:
            self.update_switch(switch)

def load_config():
    with open("phone_config.json") as json_file:
        data = json.load(json_file)
    return data

server = Server(load_config())

def get_filename(sensor):
    return sensor + "_" + int(time.time())

app = Flask(__name__)
@app.route("/upload", methods=['POST'])
def handle_upload():
    sensor = request.form['sensor']
    if "file" not in request.files:
        return Response(json.dumps({"error": "missing file"}), status=400)

    files = request.files.getlist("file")
    data = get_filename()
    files[0].save(data)

    server.process_data(sensor, data)
    return "Recieved"

@app.route("/")
def hello():
    return "I am the server!"

def main():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
