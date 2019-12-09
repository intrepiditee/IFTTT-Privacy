import subprocess

PATH = ''


def _encrypt(pt):
    p = subprocess.Popen(["./sealexamples", "3", pt], stdout=subprocess.PIPE)
    return p.communicate()[0]


def encrypt_to_file(pt, filename):
    filename = PATH + filename
    f = open(filename, "w")
    f.write(_encrypt(pt))
    return filename


def encrypt(data, filename):
    encrypt_to_file(hex(data)[2:], filename)
