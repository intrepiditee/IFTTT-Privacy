import time
import subprocess
import random
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
    print(bios)
    args = ["./sealexamples", "4"] + filenames
    print(args)
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    b = BytesIO(p.communicate()[0])
    return b


def h_diff(a, b):
    print('-', a, b, type(a), type(b))
    filename1, filename2 = cache_bytesio(a), cache_bytesio(b)
    p = subprocess.Popen(["./sealexamples", "1", filename1, filename2], stdout=subprocess.PIPE)
    b = BytesIO()
    b.write(p.communicate()[0])
    return b
