import subprocess
import time;



def encrypt(pt):
	p = subprocess.Popen(["./sealexamples", "3", pt], stdout=subprocess.PIPE)
	return p.communicate()[0]

#Default implementation in the library, if you use encrypt, change the library and recompile
def encrypt_to_file(pt):
	filename = "op" + pt + str(time.time()) + ".txt"
	f = open(filename, "w")
	f.write(encrypt(pt));
	return filename


def decrypt_from_file(filename):
	p = subprocess.Popen(["./sealexamples", "2", filename], stdout=subprocess.PIPE)
	print p.communicate()[0];
	
def subtract(a, b):
	p = subprocess.Popen(["./sealexamples", "1", a, b], stdout=subprocess.PIPE)
	f = open("result.txt" + datetime.now().hour + datetime.now().minute())
	f.write(p.communicate()[0]);
	
#Default implementation in the library, if you use encrypt, change the library and recompile
# takes two files and stored result in a new result* file
def subtract_two_files(filename_a, filename_b):
	filename = "result_subtract" + str(time.time()) + ".txt"
	p = subprocess.Popen(["./sealexamples", "1", filename_a, filename_b], stdout=subprocess.PIPE)
	f = open(filename, "w+")
	f.write(p.communicate()[0])
	
	return filename

def add_multiple(arr):
	filename = "result_add_multiple" + str(time.time()) + ".txt"
	p = subprocess.Popen(["./sealexamples", "4", arr[0], arr[1], arr[2]], stdout=subprocess.PIPE)
	f = open(filename, "w+")
	f.write(p.communicate()[0])	
	#print p.communicate()[0]
	return filename



# Sensor sends the data stored in variables a and b, a and b are filenames
a = encrypt_to_file("A");
b = encrypt_to_file("F");
c = encrypt_to_file("F");

#a = "opA1571758416.06.txt" 
#b = "opF1571758416.14.txt" 
#c = "opF1571758416.22.txt"

#print a,b ,c
decrypt_from_file(a);
decrypt_from_file(b);
#decrypt_from_file(c);

## server recieves data
#print subtract_two_files(a, b)
#print add_multiple([a, b, c])
#decrypt_from_file("result_add_multiple1571760146.18.txt");
#decrypt_from_file(subtract_two_files(a, b))
decrypt_from_file(add_multiple([a, b, c]));

	