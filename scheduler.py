# @Author: allen
# @Date: May 30 19:50 2020
import time
import sys

import schedule

from qqmusic_cookie_setter import main, logging


if __name__ == '__main__':
    # Get the time when run command as "python3 scheduler.py HH:SS"
    if len(sys.argv) > 1:
        sche_times = sys.argv[1:]
    else:
        # Run every day at 05:18, 13:18, 21:18
        sche_times = ['05:18', '13:18', '21:18']

    for t in sche_times:
        logging.info(schedule.every().day.at(t).do(main))
    # Run schedule task forever.
    while 1:
        schedule.run_pending()
        time.sleep(1)
