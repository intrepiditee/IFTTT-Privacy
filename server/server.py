from flask import Flask, request, Response
import requests
from collections import defaultdict, deque
from homomorphic_computations import *
import json
import itertools
import time
import threading
import os
import io
from configurer import Configurer


class DataCache:
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


class Computation:
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
            if not data_cache.has_value(dp):
                print("ERROR: value not in data cache:", dp)
                return None
            elif data_cache.get_value(dp) == None:
                print("ERROR: value not in data cache:", dp)
                return None
        if self.computation_type == "ident":
            return data_cache.get_value(self.datapoints[0])
        elif self.computation_type == "+":
            bios = [data_cache.get_value(dp) for dp in self.datapoints if data_cache.has_value(dp)]
            if len(bios) != len(self.datapoints):
                return None

            result = h_sum(*bios)
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
            if data[0] == None or data[1] == None:
                return None
            result = h_diff(data[1], data[0])
            for i in range(1, len(data) - 1):
                if data[i + 1] == None:
                    return None
                result = h_sum(result, h_diff(data[i + 1], data[i]))
            return result
        elif self.computation_type == "run_sum":
            data = data_cache.get_range(self.datapoints[0], self.num)
            result = data[0]
            for i in range(1, len(data)):
                if data[i] == None:
                    break
                result = h_sum(result, data[i])
            return result
        else:
            print("ERROR: unknown computation type", self.computation_type)

    def __str__(self):
        return self.computation_type + "(" + ",".join(self.datapoints) + ")" + (
            "" if self.computation_type != "rate" and self.computation_type != "run_sum" else "(" + str(
                self.num) + ")") + "->" + ",".join(self.output)



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

        self.num_switches = config["num_switches"]
        self.switch_to_address = {}
        self.lock = threading.Lock()


    def configure_switch_to_address(self, switch, address):
        self.lock.acquire()
        self.switch_to_address[switch] = address
        self.lock.release()


    def get_num_switches(self):
        self.lock.acquire()
        num = len(self.switch_to_address)
        self.lock.release()
        return num

    def update_switch(self, switch):
        print("Updating switch", switch, "w/ data", ",".join(self.switch_to_datapoints[switch]))
        failed = False
        for dp in self.switch_to_datapoints[switch]:
            if not self.data_cache.has_value(dp) or not self.data_cache.get_value(dp):
                print("ERROR: failed sending to switch", switch, ", not enough data, missing", dp)
                failed = True
                break
            with open(dp, 'wb+') as f:
                data = self.data_cache.get_value(dp).getvalue()
                f.write(data)
        if failed:
            return
        files = [('file', open(datapoint, 'rb')) for datapoint in self.switch_to_datapoints[switch]]

        print("Post to switch")
        requests.post(self.switch_to_address[switch], files=files)

    def process_data(self, sensor, value):
        print("Processing data from", sensor)
        self.data_cache.add_value(sensor, value)
        affected_switches = set([])
        for computation in self.sensor_to_computations[sensor]:
            print("Computing", str(computation))
            result = computation.compute(self.data_cache)
            if result:
                self.data_cache.add_value(computation.name, result)
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



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "."


server = Server(load_config())

sensor_configurer = Configurer("sensor_config.json", "sensors")
switch_configurer = Configurer("switch_config.json", "switches")


def get_filename(sensor):
    return sensor + "_" + str(int(time.time()))


@app.route("/upload", methods=['POST'])
def handle_upload():

    if server.get_num_switches() != server.num_switches:
        return Response(json.dumps({"error": "switches not configured yet"}), status=500)

    if "file" not in request.files:
        print("ERROR: missing file")
        return Response(json.dumps({"error": "missing file"}), status=400)

    files = request.files.getlist("file")
    sensor = files[0].filename
    data = files[0].read()
    filedata = io.BytesIO(data)

    server.process_data(sensor, filedata)

    return "Recieved"


@app.route("/configure/sensor", methods=['GET'])
def configure_sensor():
    config = sensor_configurer.get()
    resp = Response(json.dumps(config), status=200, mimetype='application/json')
    return resp



@app.route("/configure/switch", methods=["GET"])
def configure_switch():
    config = switch_configurer.get()
    resp = Response(json.dumps(config), status=200, mimetype='application/json')
    server.configure_switch_to_address(
        "switch" + str(server.get_num_switches() + 1),
        'http://' + request.remote_addr + ':8080/update'
    )
    return resp


def main():
    app.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
