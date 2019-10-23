from crypto import decrypt_from_file


def decrypt(filename):
    return int(decrypt_from_file(filename), 16)
