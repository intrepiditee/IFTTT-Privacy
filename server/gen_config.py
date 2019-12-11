import json
import sys
import random

random.seed(0)

num = 3
if len(sys.argv) > 1:
    num = int(sys.argv[1])

sensor_config = {"sensors": []}
switch_config = {"switches": []}
server_config = {"computations": [], "num_switches": num}

sensors = ["ifttt_sensor_" + str(i) for i in range(1, num + 1)]
switches = ["switch" + str(i) for i in range(1, num + 1)]

for i in range(1, num + 1):
    server_config["computations"].append({"type": "+", "datapoints": sensors, "name": "avg_temp_" + str(i), "output": ["switch" + str(i)]})

min_sum = 0
max_sum = 0

for i in range(1, num + 1):
    min_num = random.randint(0, int(256 / (2 * num + 4)))
    max_num = random.randint(min_num + 1, int(256 / (num + 2)))
    min_sum += min_num
    max_sum += max_num
    interval = 10#random.randint(1,30)
    sensor_config["sensors"].append({"name": "ifttt_sensor_" + str(i), "min": min_num, "max": max_num, "interval": interval})

for i in range(1, num + 1):
    pivot = random.randint(min_sum, max_sum)
    switch_config["switches"].append({"name": "ifttt_switch_" + str(i), "rules": [{"output": 1, "conditions": [{"name": "avg_temp_" + str(i), "operand": "<", "value": pivot}]}, {"output": 2, "conditions": [{"name": "avg_temp_" + str(i), "operand": "=", "value": pivot}]}, {"output": 3, "conditions": [{"name": "avg_temp_" + str(i), "operand": ">", "value": pivot}]}]})

print(sensor_config)
print("\n\n\n\n")
print(switch_config)
print("\n\n\n\n")
print(server_config)

with open("sensor_config.json", "w") as f:
    f.write(json.dumps(sensor_config, sort_keys=True, indent=4))

with open("switch_config.json", "w") as f:
    f.write(json.dumps(switch_config, sort_keys=True, indent=4))

with open("phone_config.json", "w") as f:
    f.write(json.dumps(server_config, sort_keys=True, indent=4))
