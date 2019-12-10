import json
import threading


class Configurer:

    def __init__(self, path, key="sensors"):
        with open(path, "rt") as f:
            configs = json.load(f)

            self.configs = configs[key]
            self.index = 0
            self.lock = threading.Lock()

    def get(self):
        self.lock.acquire()

        config = self.configs[self.index];
        self.index += 1
        if self.index >= len(self.configs):
            self.index = 0

        self.lock.release()

        return config