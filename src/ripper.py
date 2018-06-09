import sys
import os
import pprint as pp

import praw
import yaml

from collections import deque

def handle(subreddit, submission, home):

    TEMP_DIR = home + ".temp/"
    
    easy_wget_prefix = ('https://i.redd.it','https://i.imgur.com','https://imgur.com')
    easy_wget_suffix = ('.jpg','.png','.gif')

    imgur_image = "https://imgur.com"
    imgur_album = "https://imgur.com/a/"
    imgur_i = "https://i.imgur.com"
    imgur_gifv = ".gifv"

    v_reddit = "https://v.redd.it"

    print("(" + submission.id + ") "
        "+" + str(submission.score).ljust(5) + ": " + submission.title
        + " (" + submission.url + ")")

    link = submission.url

    # Easy links that we can just download directly
    if link.startswith(easy_wget_prefix) and link.endswith(easy_wget_suffix):
        print("Found an easy wget link")
        return

    # Either an album or another imgur thing that we just need to process
    if link.startswith(imgur_image): 
        if not link.startswith(imgur_album):
            print("Found imgur append .png -> wget")
            return
        elif link.startswith(imgur_album):
            print("Found an imgur album")
            return
    
    # A gifv!
    if link.startswith(imgur_i) and link.endswith(imgur_gifv):
        print("Found a gifv....")
        return

    # A video. This is our last option.
    if link.startswith(v_reddit):
        print("Found a video!")
        return

    return
    

def rip(config, history, home):

    reddit = praw.Reddit(client_id=config['reddit']['client_id'],
                         client_secret=config['reddit']['client_secret'],
                         user_agent='headless')

    # Get list of subreddits and convert their titles to lower case
    subreddits = config['subreddits']
    history = {k.lower(): v for k, v in history.items()}
    

    # Now go through them and do their dirty deeds
    for sbr in subreddits:

        name = sbr['name'].lower()

        ## PROCESS CONFIG ##

        # Get the values for searching and execution
        threshold = sbr['threshold'] if 'threshold' in sbr else config['global']['threshold']
        limit = sbr['limit'] if 'limit' in sbr else config['global']['limit']
        rclone = sbr['rclone'] if 'rclone' in sbr else config['global']['rclone']

        # Filters is a bit of a special case
        # We need an unprocessed version and a processed version
        filters = None
        if 'filters' in sbr:
            filters = sbr['filters']
        elif 'filters' in config['global']:
            filters = config['global']['filters']
        
        # Convert everything to lower case
        if filters:
            filters = [filth.lower() for filth in filters]

        ## PROCESS HISTORY ##
        # Index: Deque with the IDs of post we've already gone through
        if name in history:
            index = deque(history[name])
        else:
            index = deque()
            
        ## The real processing starts here ##

        subreddit = reddit.subreddit(name)
    
        print(subreddit.display_name)
        print("Excluding: " + str(filters))
        for submission in subreddit.hot(limit=limit):
            if submission.score < threshold: continue
            if submission.stickied: pass
            if "redd.it" not in submission.url and "imgur" not in submission.url: continue

            # Because we're in a double nested for loop, raise an exception from inside to trigger
            # outside to run a continue loop
            # Scan all filters and make sure matching filters are excluded
            try:
                for filth in filters:
                    if filth in submission.title.lower():
                        raise Exception()
            except:
                continue

            # Check IDs
            if submission.id in index: continue

            # We're done with checking, process the post now

            handle(subreddit, submission, home)

        print()

    # This is where the for loop ends
