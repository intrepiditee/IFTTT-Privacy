import time
import subprocess

def make_filename(a, b):
    return "computation_" + str(abs(hash(a)))[:-4] + "_" + str(abs(hash(b)))[:-4] + "_" + str(int(time.time()))[:-6]

def h_sum(a, b):
    print('+', a, b, type(a), type(b))
    name = make_filename(a, b)
    p = subprocess.Popen(["./sealexamples", "1", a, b], stdout=subprocess.PIPE)
    f = open(name, 'wb+')
    f.write(p.communicate()[0])
    f.close()
    return name

def h_diff(a, b):
    print('-', a, b, type(a), type(b))
    name = make_filename(a, b)
    p = subprocess.Popen(["./sealexamples", "1", a, b], stdout=subprocess.PIPE)
    f = open(name, 'wb+')
    f.write(p.communicate()[0])
    f.close()
    return name

def h_prod(a, b):
    print('*', a, b, type(a), type(b))
    name = make_filename(a, b)
    p = subprocess.Popen(["./sealexamples", "1", a, b], stdout=subprocess.PIPE)
    f = open(name, 'wb+')
    f.write(p.communicate()[0])
    f.close()
    return name
