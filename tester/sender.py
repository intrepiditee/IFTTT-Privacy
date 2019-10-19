import requests

def read_tests():
    sensor_to_data = {}
    with open('tests.tsv', "rt") as f:
        next(f)
        for line in f:
            fields = line.split()
            sensor = fields[0]
            data = fields[1]
            sensor_to_data[sensor] = data
    return sensor_to_data

def send_requests(sensor_to_data):
    for sensor, data in sensor_to_data.items():
        print("Sent " + data + "!")
        requests.post("http://ifttt_sensor_" + sensor + ":8080/send", data={"data": data})

def main():
    send_requests(read_tests())

if __name__ == "__main__":
    main()