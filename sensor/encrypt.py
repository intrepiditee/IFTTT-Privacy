from crypto import encrypt_to_file

def encrypt(data, filename):
    encrypt_to_file(hex(data)[2:], filename)