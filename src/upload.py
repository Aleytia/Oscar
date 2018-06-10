import os
import sys
import pprint as pp

import datetime
import yaml

from shlex import quote
from collections import deque

def upload(rclone, temp_dir, days):
    """
    Get subreddit name and sbr config, and upload to destination using rclone

    We know everything we want is in ~home/.temp/

    rclone copy temp_dir $RCLONE[x]/2018-06/(DAY/)
    """

    time = datetime.datetime.now()
    BASE_DATE = str(time.year) + '.' + str(time.month).zfill(2)
    DAY = '/' + str(time.day).zfill(2)

    command = "rclone copy " + quote(temp_dir) + " "
    for end in rclone:
        if not days:
            if end.endswith('/'):
                os.system(command + end + BASE_DATE + " -v")
            else:
                os.system(command + end + '/' + BASE_DATE + " -v")
        elif days:
            if end.endswith('/'):
                os.system(command + end + BASE_DATE + DAY + " -v")
            else:
                os.system(command + end + '/' + BASE_DATE + DAY + " -v")

