# @Author: allen
# @Date: May 20 15:50 2020
import base64
import random
import time
from functools import wraps
from getpass import getpass

import schedule
import requests
from selenium import webdriver


WEBDRIVER = 'drivers/chromedriver'
TIMEOUT = 20
USERNAME = '337657561'
ENCODED_PASSWORD = '6NDhyuTe2c_ZzOPe'
SET_COOKIE = 'http://cn.lonsty.me:8179/user/setCookie'
SECRET_KEY = None
PASSWORD = None


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


def encode(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    encoded_string = encoded_string.encode('latin')
    return base64.urlsafe_b64encode(encoded_string).rstrip(b'=')


def decode(key, string):
    string = base64.urlsafe_b64decode(string + b'===')
    string = string.decode('latin')
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string


@retry(Exception)
def login_for_cookies() -> dict:
    """
    Login to y.qq.com via selenium
    :return: dict, user cookies
    """
    # Use Google Chrome driver
    driver = webdriver.Chrome('drivers/chromedriver')
    # Open https://y.qq.com in Chrome
    driver.get('https://y.qq.com')
    # Open login page
    driver.find_element_by_link_text('登录').click()

    # Switch to the top window
    driver.switch_to.window(driver.window_handles[-1])

    # Switch to the login iframe step by step
    while 1:
        try:
            driver.switch_to.frame('frame_tips')  # iframe frame_tips
            break
        except Exception:
            time.sleep(0.5)

    while 1:
        try:
            driver.switch_to.frame('ptlogin_iframe')  # iframe ptlogin_iframe
            break
        except Exception:
            time.sleep(0.5)

    time.sleep(3)
    # Switch to input popup, fill username and password, then login
    driver.find_element_by_id('switcher_plogin').click()
    driver.find_element_by_name('u').send_keys(USERNAME)
    driver.find_element_by_name('p').send_keys(decode(SECRET_KEY, ENCODED_PASSWORD.encode()))
    driver.find_element_by_id('login_button').click()

    # Check if login is successful by checking cookie value of qm_keyst
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


def set_api_cookies(cookies: dict):
    """
    Set cookies to QQ Music API server.
    :param cookies: dict, user cookies
    :return: bool, True if set succeed.
    """
    # Convert dict cookies to string
    cookies_str = '; '.join([f'{k}={v}' for k, v in cookies.items()])
    # The body data of POST
    body = {'data': cookies_str}
    # Must give a user-agent header to bypass API server detection
    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}

    resp = requests.post(SET_COOKIE, json=body, headers=headers, timeout=TIMEOUT)
    if resp.status_code == 200 and resp.json().get('result') == 100:
        return True
    else:
        print(f'Cookies set failed.\nStatus Code: {resp.status_code}\nText: {resp.text}')


def main():
    cookies = login_for_cookies()
    result = set_api_cookies(cookies)
    if result:
        print(f'Cookies set successfully at {time.ctime()}')


if __name__ == '__main__':
    SECRET_KEY = getpass('Input the secret key to decode password: ')

    schedule.every().day.at("5:18").do(main)
    while 1:
        schedule.run_pending()
        time.sleep(1)
