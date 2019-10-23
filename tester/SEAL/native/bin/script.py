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
	filename = "result" + str(time.time()) + ".txt"
	p = subprocess.Popen(["./sealexamples", "1", filename_a, filename_b], stdout=subprocess.PIPE)
	f = open(filename, "w+")
	f.write(p.communicate()[0])
	
	return filename




# Sensor sends the data stored in variables a and b, a and b are filenames
a = encrypt_to_file("AE");
b = encrypt_to_file("F");


#decrypt_from_file(a);
#decrypt_from_file(b);

## server recieves data
print subtract_two_files(a, b)

decrypt_from_file(subtract_two_files(a, b));

	