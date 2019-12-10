import time
import subprocess
import random
import os
from io import BytesIO

def make_filename():
    return "tmp" + str(random.randint(0, 1024)) + str(time.time())

def cache_bytesio(bio):
    filename = make_filename()
    with open(filename, "wb+") as f:
        encrypted = bio.getvalue()
        f.write(encrypted)
    return filename

def h_sum(*bios):
    filenames = [cache_bytesio(bio) for bio in bios]
    args = ["./sealexamples", "4"] + filenames
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    b = BytesIO(p.communicate()[0])
    try:
        for filename in filenames:
            os.remove(filename)
    except:
        print("ERROR: failed removing filenames: [" + ",".join(filenames) + "]")
    return b

def h_diff(*bios):
    filenames = [cache_bytesio(bio) for bio in bios]
    args = ["./sealexamples", "1"] + filenames
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    b = BytesIO(p.communicate()[0])
    try:
        for filename in filenames:
            os.remove(filename)
    except:
        print("ERROR: failed removing filenames: [" + ",".join(filenames) + "]")
    return b
