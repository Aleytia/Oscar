import sys
import os

import yaml
import pprint as pp


def load_config(path):

    # Either a global fallback needs to exist, or every subreddit needs these options
    NO_GLOBAL_RCLONE = False
    NO_GLOBAL_THRESHOLD = False
    NO_GLOBAL_LIMIT = False

    try:
        with open(path, 'r') as cfyml:
            try:
                config = yaml.load(cfyml)
            except:
                raise Exception("A bad config file was provided.")
    except:
        raise Exception("Config file either does not exist or is unavailable.")

    # Make sure we have credentials
    rdt = config['reddit']
    if "client_id" not in rdt: raise Exception("Missing client_id")
    if "client_secret" not in rdt: raise Exception("Missing client_secret")

    # Make sure every subreddit has sufficient information
    gbl = config['global']
    if "threshold" not in gbl: NO_GLOBAL_THRESHOLD = True
    if "rclone" not in gbl: NO_GLOBAL_RCLONE = True
    if "limit" not in gbl: NO_GLOBAL_LIMIT = True

    for subreddit in config['subreddits']:
        """
        Check if necessary fields exist, and that no space exists for the subreddit name.
        """
        if "name" not in subreddit: raise Exception("No name provided.")
        if " " in subreddit['name']: raise Exception("Multiple word subreddit detected.")
        
        if NO_GLOBAL_RCLONE:
            if "rclone" not in subreddit: 
                raise Exception("Missing rclone path in r/" + subreddit['name'])
        if NO_GLOBAL_THRESHOLD:
            if "threshold" not in subreddit: 
                raise Exception("Missing threshold in r/" + subreddit['name'])
        if NO_GLOBAL_LIMIT:
            if "limit" not in subreddit:
                raise Exception("Missing threshold in r/" + subreddit['name'])

    return config


def load_history(path):

    try:
        with open(path, 'r') as hsyml:
            try:
                history = yaml.load(hsyml)
            except:
                raise Exception("A bad history file was provided.")
    except:
        return dict()

    # Just a quick check to return a list if empty
    if history is None: history = dict()

    # We assume history file is good, since it's machine edited
    return history

