# @Author: allen
# @Date: May 20 15:50 2020
import time
from getpass import getpass

import schedule

from qqmusic_cookie_setter import main


if __name__ == '__main__':
    schedule.every().day.at("5:18").do(main)
    while 1:
        schedule.run_pending()
        time.sleep(1)
