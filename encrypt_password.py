# @Author: allen
# @Date: May 30 19:38 2020
from getpass import getpass

import yaml

from qqmusic_cookie_setter import encode

if __name__ == '__main__':
    try:
        with open('settings.yml', 'r') as f:
            settings = yaml.load(f, yaml.Loader)
    except FileNotFoundError:
        settings = {}

    username = input('Username: ')
    try:
        username = int(username)
    except ValueError:
        pass
    password = getpass('Password: ')
    secret_key = getpass('Secret Key: ')
    encoded_password = encode(secret_key, password).decode()

    settings.update({'username': username,
                     'password': '******',
                     'secret_key': secret_key,
                     'encoded_password': encoded_password})

    with open('settings.yml', 'w') as f:
        yaml.dump(data=settings, stream=f, sort_keys=False)
