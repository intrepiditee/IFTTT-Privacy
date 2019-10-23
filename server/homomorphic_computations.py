import time
import subprocess
import random
from io import BytesIO

def make_filename(a, b):
    return "tmp" + str(random.randint(0,1024)) + str(time.time())

def cache_bytesio(bio):
    filename = "tmp" + str(random.randint(0,1024)) + str(time.time())
    with open(filename, "wb+") as f:
        f.write(bio.read())
    return filename

def h_sum(a, b):
    print('+', a, b, type(a), type(b))
    filename1, filename2 = cache_bytesio(a), cache_bytesio(b)
    p = subprocess.Popen(["./sealexamples", "1", filename1, filename2], stdout=subprocess.PIPE)
    b = BytesIO()
    b.write(p.communicate()[0])
    return b

def h_diff(a, b):
    print('-', a, b, type(a), type(b))
    filename1, filename2 = cache_bytesio(a), cache_bytesio(b)
    p = subprocess.Popen(["./sealexamples", "1", filename1, filename2], stdout=subprocess.PIPE)
    b = BytesIO()
    b.write(p.communicate()[0])
    return b

def h_prod(a, b):
    print('*', a, b, type(a), type(b))
    filename1, filename2 = cache_bytesio(a), cache_bytesio(b)
    p = subprocess.Popen(["./sealexamples", "1", filename1, filename2], stdout=subprocess.PIPE)
    b = BytesIO()
    b.write(p.communicate()[0])
    return b
