import sys
import os
import pprint as pp

import re
import datetime

from collections import deque
from shlex import quote

def standard(subreddit, submission, sbr_config, temp_dir, days, repeats):
    """
    We only want to download files here. 
    rclone.py will take care of the rest, and we'll clean up files separately.
    """

    name = submission.title
    if repeats: name = name + " (" + submission.id + ")" # Add IDs if non-unique names
    name = name + ".png"
    name = name.replace('/', ' ') # Replace / charcters

    url = submission.url + ".png"

    os.system("/usr/bin/wget " + url + " -O " + quote(temp_dir + name))

def album(subreddit, submission, sbr_config, temp_dir, days, repeats):
    
    name = submission.title
    if repeats: name = name + " (" + submission.id + ")"

    zip_name = name + ".zip"
    zip_name = zip_name.replace('/', ' ')

    name = name.replace('/', ' ')

    url = submission.url + "/zip"

    os.system("/usr/bin/wget " + url + " -O " + quote(temp_dir + zip_name))
    os.system("/usr/bin/unzip " + quote(temp_dir + zip_name) + " -d " + quote(temp_dir + name))
    os.system("/bin/rm " + quote(temp_dir + zip_name))

def gifv(subreddit, submission, sbr_config, temp_dir, days, repeats):
    
    name = submission.title
    if repeats: name = name + " (" + submission.id + ")"
    name = name + ".gif"
    name = name.replace('/', ' ')

    url = submission.url[:-5] + ".gif"

    os.system("/usr/bin/wget " + url + " -O " + quote(temp_dir + name))


