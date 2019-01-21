import sys
import os
import pprint as pp

import re
import datetime

from collections import deque
from shlex import quote

def easy(subreddit, submission, sbr_config, temp_dir, days, repeats):
    """
    We only want to download files here. 
    rclone.py will take care of the rest, and we'll clean up files separately.
    """

    time = datetime.datetime.now()
    folder = str(time.year) + "-" + str(time.month).zfill(2)

    name = submission.title 
    if repeats: name = name + " (" + submission.id + ")" # Add IDs if non-unique names
    name = name + submission.url[-4:]
    name = name.replace('/', ' ') # Replace / characters for Windows
    
    # Let's use wget and not requests for this
    os.system("/usr/bin/wget " + submission.url + " -O " + quote(temp_dir + name))
