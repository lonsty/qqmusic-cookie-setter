#!/usr/bin/env bash
# Type `crontab -e` in the terminal, then add following line to it:
# @reboot export https_proxy=https://user:pwd@host:port /path/to/entrypoint.sh

/home/allen/.local/share/virtualenvs/qqmusic-cookie-setter-Vp3S7ezg/bin/python /mnt/data/workspace/git/packages/qqmusic-cookie-setter/scheduler.py
