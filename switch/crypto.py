import subprocess
import time


PATH = '/usr/src/app/'

def encrypt(pt):
	p = subprocess.Popen(["." + PATH + "sealexamples", "3", pt], stdout=subprocess.PIPE)
	return p.communicate()[0]

#Default implementation in the library, if you use encrypt, change the library and recompile
def encrypt_to_file(pt):
	filename = 'PATH' + "op" + pt + str(time.time()) + ".txt"
	f = open(filename, "w")
	f.write(str(encrypt(pt)))
	return filename


def decrypt_from_file(filename):
	p = subprocess.Popen(["." + PATH + "sealexamples", "2", filename], stdout=subprocess.PIPE)
	return(p.communicate()[0])
	
def subtract(a, b):
	p = subprocess.Popen(["." + PATH + "sealexamples", "1", a, b], stdout=subprocess.PIPE)
	f = open("result.txt" + datetime.now().hour + datetime.now().minute())
	f.write(str(p.communicate()[0]))
	
#Default implementation in the library, if you use encrypt, change the library and recompile
# takes two files and stored result in a new result* file
def subtract_two_files(filename_a, filename_b):
	filename = PATH + "result" + str(time.time()) + ".txt"
	p = subprocess.Popen(["./SEAL/native/bin/sealexamples", "1", filename_a, filename_b], stdout=subprocess.PIPE)
	f = open(filename, "w+")
	f.write(str(p.communicate()[0]))
	
	return filename

