import sys
import os
import pprint as pp

import re
import datetime
import requests

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
    
    # Let's use /usr/bin/wget and not requests for this
    os.system("/usr/bin/wget " + submission.url + " -O " + quote(temp_dir + name))


def video(subreddit, submission, sbr_config, temp_dir, days, repeats):
    name = submission.title
    if repeats: name = name + " (" + submission.id + ")"
    name = name + ".mp4"
    name = name.replace('/', ' ')

    try:
        video_url = submission.media['reddit_video']['fallback_url']
        audio_url = submission.url + "/audio"
    except:
        print("Error with submission, skipping...")
        return

    audio = requests.get(audio_url)
    if audio.status_code != 200:
        os.system("/usr/bin/wget " + video_url + " -O " + quote(temp_dir + name))
        return

    # There IS an audio track
    os.system("/usr/bin/wget " + video_url + " -O " + quote(temp_dir + submission.id + ".mp4"))
    os.system("/usr/bin/wget " + audio_url + " -O " + quote(temp_dir + submission.id + ".mp3"))
    os.system("/usr/bin/ffmpeg -i " + quote(temp_dir) + 
            submission.id + ".mp4 -i " + quote(temp_dir) + 
            submission.id + ".mp3 -c copy -y " + 
            quote(temp_dir + name))
    os.system("/bin/rm " + quote(temp_dir) + submission.id + ".mp4 " + quote(temp_dir) + submission.id + ".mp3")
