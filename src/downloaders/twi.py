import sys
import os
import pprint as pp

import re
import datetime

from collections import deque
from shlex import quote

def image(subreddit, submission, sbr_config, temp_dir, days, repeats):
	name = submission.title
	if repeats: name = name + " (" + submission.id + ")" # Add ids

	ext_url = submission.url.replace("?name=orig","")
	_, ext = os.path.splitext(ext_url)

	name = name + ext
	name = name.replace('/', ' ') # Replace bad characters

	print("Saving to " + quote(temp_dir + name))
	os.system("/usr/bin/wget " + submission.url + " -O " + quote(temp_dir + name))

	print()

    

