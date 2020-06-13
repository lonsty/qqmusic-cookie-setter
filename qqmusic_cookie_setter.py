# @Author: allen
# @Date: May 30 19:31 2020
import base64
import logging
import random
import time
import sys
from functools import wraps
from getpass import getpass
from pathlib import PurePath

import requests
import yaml
from selenium import webdriver

HOST = 'https://y.qq.com'
GET_COOKIE_API = 'https://api.qq.jsososo.com/user/cookie'
SET_COOKIE_API = 'http://cn.lonsty.me:8179/user/setCookie'
WEBDRIVER = 'drivers/chromedriver'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
TIMEOUT = 20
SETTINGS = {}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(PurePath(__file__).parent.joinpath('scheduler.log')),
        logging.StreamHandler()
    ]
)


def retry(exceptions, tries=3, delay=1, backoff=2, logger=None):
    """
    Retry calling the decorated function using an exponential backoff.
    Args:
        exceptions: The exception to check. may be a tuple of
            exceptions to check.
        tries: Number of times to try (not retry) before giving up.
        delay: Initial delay between retries in seconds.
        backoff: Backoff multiplier (e.g. value of 2 will double the delay
            each retry).
        logger: Logger to use. If None, print.
    """

    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay or random.uniform(0.5, 1.5)
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    if logger:
                        logger.warning('{}, Retrying in {} seconds...'.format(e, mdelay))
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry

    return deco_retry


def encode(key: str, string: str) -> str:
    """
    Encrypt password with secret key.

    :param key: str, secret key.
    :param string: str, password.
    :return: str, encrypted password.
    """
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    encoded_string = encoded_string.encode('latin')
    return base64.urlsafe_b64encode(encoded_string).rstrip(b'=').decode()


def decode(key: str, string: str) -> str:
    """
    Decrypt password with secret key.

    :param key: str, secret key.
    :param string: str, encrypted password.
    :return: str, password.
    """
    string = base64.urlsafe_b64decode(string.encode() + b'===')
    string = string.decode('latin')
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string


def read_and_encrypt_settings() -> dict:
    """
    read settings from input or settings file, and save the encrypted settings to file.

    :return: dict, key-value settings.
    """
    # Try to read settings from file.
    try:
        with open('settings.yml', 'r') as f:
            settings = yaml.load(f, yaml.Loader)
    except FileNotFoundError:
        settings = {}

    # If the settings file dose not exist, ask the user to enter in terminal.
    if not settings:
        webdriver_ = input(f'Path of chromedriver({WEBDRIVER}): ') or WEBDRIVER
        set_cookie_api = input(f'Set cookie API({SET_COOKIE_API}): ') or SET_COOKIE_API

        username = input('Username: ')
        try:
            username = int(username)
        except ValueError:
            pass
        password = getpass('Password: ')
        secret_key = getpass('Secret Key: ')
        encoded_password = encode(secret_key, password)

        settings.update({'webdriver': webdriver_,
                         'set_cookie_api': set_cookie_api,
                         'username': username,
                         'password': '******',
                         'secret_key': secret_key,
                         'encoded_password': encoded_password})
        # Write new settings to file.
        with open('settings.yml', 'w') as f:
            yaml.dump(data=settings, stream=f, sort_keys=False)

    # If user edit password via settings file, hide it and create an encrypted password.
    if settings.get('password') != '******':
        settings.update({'password': '******',
                         'encoded_password': encode(settings.get('secret_key'),
                                                    settings.get('password'))})
        # Write changes to file.
        with open('settings.yml', 'w') as f:
            yaml.dump(data=settings, stream=f, sort_keys=False)

    return settings


@retry(Exception, logger=logging)
def login_for_cookies() -> dict:
    """
    Login to y.qq.com via selenium.

    :return: dict, user cookies.
    """
    # Use Google Chrome driver.
    driver = webdriver.Chrome(SETTINGS.get('webdriver', WEBDRIVER))
    driver.get(HOST)
    # Open login page.
    driver.find_element_by_link_text('登录').click()
    # Switch to the top window.
    driver.switch_to.window(driver.window_handles[-1])
    # Switch to the login iframe step by step.
    while 1:
        try:
            driver.switch_to.frame('frame_tips')  # iframe frame_tips.
            break
        except Exception:
            time.sleep(0.5)

    while 1:
        try:
            driver.switch_to.frame('ptlogin_iframe')  # iframe ptlogin_iframe.
            break
        except Exception:
            time.sleep(0.5)

    time.sleep(3)
    # Switch to input popup, fill username and password, then login.
    driver.find_element_by_id('switcher_plogin').click()
    driver.find_element_by_name('u').send_keys(SETTINGS.get('username'))
    driver.find_element_by_name('p').send_keys(decode(SETTINGS.get('secret_key'),
                                                      SETTINGS.get('encoded_password')))
    driver.find_element_by_id('login_button').click()

    # Check if login is successful by checking value of qm_keyst in cookies.
    time_cost = 0
    while 1:
        cookies_list = driver.get_cookies()
        cookies_dict = {item.get('name'): item.get('value') for item in cookies_list}
        if cookies_dict.get('qm_keyst'):
            break
        if time_cost > TIMEOUT:
            raise TimeoutError('Login timeout.')
        time.sleep(0.5)
        time_cost += 0.5
    driver.quit()

    return cookies_dict


@retry(Exception)
def get_api_cookies() -> dict:
    """
    Get public cookies by cookie api.

    :return: dict, key-value cookies.
    """
    resp = requests.get(GET_COOKIE_API, headers=HEADERS, timeout=TIMEOUT)
    if resp.status_code == 200 and resp.json().get('result') == 100:
        return resp.json().get('data').get('userCookie')
    else:
        raise Exception('Get cookies failed')


@retry(Exception)
def set_api_cookies(cookies: dict):
    """
    Set cookies to QQ Music API server.

    :param cookies: dict, user cookies
    :return: bool, True if set succeed.
    """
    # Convert dict cookies to string.
    cookies_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
    body = {'data': cookies_str}
    resp = requests.post(SETTINGS.get('set_cookie_api', SET_COOKIE_API),
                         json=body, headers=HEADERS, timeout=TIMEOUT)
    if resp.status_code == 200 and resp.json().get('result') == 100:
        return True
    else:
        raise Exception(f'Cookies set failed.\nStatus Code: {resp.status_code}\nText: {resp.text}')


def main():
    try:
        cookies = get_api_cookies()
        result = set_api_cookies(cookies)
        if result:
            logging.info(f'Cookies set successfully at {time.ctime()}')
    except KeyboardInterrupt:
        logging.info('KeyboardInterrupt')
    except Exception as e:
        logging.error(e)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
