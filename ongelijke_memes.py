from urllib.request import urlretrieve
from time import sleep
import praw

import config

R = None  # This will be a global reddit instance
FORMATS = {".gif": ".gif", ".png": ".png", "jpeg": ".jpeg", ".jpg": ".jpg"}
PATH_MEMES = "C:\\Users\\Jochem\\Pictures\\Memes\\"

def bot_login():
    reddit = praw.Reddit(username = config.username,
                         user_agent = config.user_agent,
                         password = config.password,
                         client_id = config.client_id,
                         client_secret = config.client_secret)
    
    return reddit

def format(url):
    if url[-4:] in FORMATS:
        return FORMATS[url[-4:]]
    return False

def extract_memes(subreddit, amount):
    subreddit = R.subreddit(subreddit)
    temp_amount = amount
    for submission in subreddit.top("day", limit=temp_amount):
        sleep(1)
        ed = format(submission.url)
        if ed:
            urlretrieve(submission.url, 
                        filename=PATH_MEMES + submission.title + ed)
        else:
            temp_amount += 1 

R = bot_login()
extract_memes("animemes", 20)
extract_memes("greentext", 20)
extract_memes("anime_irl", 10)
