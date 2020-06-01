# @Author: allen
# @Date: May 30 19:50 2020
import time
import sys

import schedule

from qqmusic_cookie_setter import main


if __name__ == '__main__':
    # Get the time when run command as "python3 scheduler.py HH:SS"
    if len(sys.argv) > 2:
        sche_time = sys.argv[1]
    else:
        sche_time = "05:18"

    print(schedule.every().day.at(sche_time).do(main))
    # Run schedule task forever.
    while 1:
        schedule.run_pending()
        time.sleep(1)
