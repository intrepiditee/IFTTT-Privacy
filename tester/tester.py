import os
import time

if __name__ == "__main__":
    os.system("python receiver.py &")
    time.sleep(2)
    os.system("python sender.py")

    while True:
        time.sleep(10)

