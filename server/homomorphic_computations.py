import time
import subprocess
import random
from io import BytesIO

def make_filename(a, b):
    return "tmp" + str(random.randint(0,1024)) + str(time.time())

def cache_bytesio(bio):
    filename = "tmp" + str(random.randint(0,1024)) + str(time.time())
    with open(filename, "wb+") as f:
        encrypted = bio.read()
        if (len(encrypted) < 10):
            raise IOError("empty")
        f.write(encrypted)
    return filename

# def h_sum(a, b):
#     print('+', a, b, type(a), type(b))
#     filename1, filename2 = cache_bytesio(a), cache_bytesio(b)
#     p = subprocess.Popen(["./sealexamples", "4", filename1, filename2], stdout=subprocess.PIPE)
#     b = BytesIO()
#     b.write(p.communicate()[0])
#     return b

def h_sum(a, b, c):
    print('+', a, b, c, type(a), type(b), type(c))
    filename1, filename2, filename3 = cache_bytesio(a), cache_bytesio(b), cache_bytesio(c)
    p = subprocess.Popen(["./sealexamples", "4", filename1, filename2, filename3], stdout=subprocess.PIPE)
    b = BytesIO()
    b.write(p.communicate()[0])
    return b

def sum(a, b, c):
    p = subprocess.Popen(["./sealexamples", "4", a, b, c], stdout=subprocess.PIPE)
    with open("avg_temp", "wb+") as f:
        f.write(p.communicate()[0])
    return "avg_temp"


def h_diff(a, b):
    print('-', a, b, type(a), type(b))
    filename1, filename2 = cache_bytesio(a), cache_bytesio(b)
    p = subprocess.Popen(["./sealexamples", "1", filename1, filename2], stdout=subprocess.PIPE)
    b = BytesIO()
    b.write(p.communicate()[0])
    return b

# def h_prod(a, b):
#     print('*', a, b, type(a), type(b))
#     filename1, filename2 = cache_bytesio(a), cache_bytesio(b)
#     p = subprocess.Popen(["./sealexamples", "1", filename1, filename2], stdout=subprocess.PIPE)
#     b = BytesIO()
#     b.write(p.communicate()[0])
#     return b
