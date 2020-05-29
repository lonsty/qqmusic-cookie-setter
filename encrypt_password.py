import base64
from getpass import getpass


def encode(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    encoded_string = encoded_string.encode('latin')
    return base64.urlsafe_b64encode(encoded_string).rstrip(b'=')


if __name__ == '__main__':
    password = getpass('Password: ')
    secret_key = getpass('Secret Key: ')
    pass_encoded = encode(secret_key, password).decode()
    print(f'')