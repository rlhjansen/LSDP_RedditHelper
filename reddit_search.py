import praw
import json
from praw.models import MoreComments

# config file contains personal information and should be handled with care
import config
from general_easyness import lprint, minput


DB_FILE = "reddit_db.json"

SUBREDDIT = ""
LIMIT = 100
T = "all"


reddit = praw.Reddit(client_id=config.client_id, client_secret=config.client_secret,
                     password=config.password, user_agent=config.user_agent,
                     username=config.username)


def search(query):
    p = {
        "q" : query,
        "limit" : LIMIT,
        "t" : T
    }

    if SUBREDDIT:
        p["restrict_sr"] = True
        return reddit.get("/r/" + SUBREDDIT + "/search", params=p)
    return reddit.get("/search", params=p)


def format_comment(comment):
    content = [comment.score, comment.body, []]
    for sub_comment in comment.replies:
        if type(sub_comment) is not MoreComments:
            content[-1].append(format_comment(sub_comment))

    return content


def format_post(post):
    content = [post.title, post.subreddit.display_name, post.upvote_ratio,
               post.score, post.selftext, []]

    for comment in post.comments:
        if (type(comment) is not MoreComments) and not comment.stickied:
            content[-1].append(format_comment(comment))

    return post.id, content


def db_add(db, post):
    key, content = format_post(post)
    db[key] = content
    return key


def db_load(filename):
    db = {}

    try:
        with open(filename) as f:
            index = f.readline()[:-1]
            if not index:
                index = None
            db = json.loads(f.readline())

    except IOError:
        index = None

    return db, index


def db_store(db, filename, index=None):
    with open(filename, "w") as f:
        if index:
            f.write(index)
        f.write('\n' + json.dumps(db))


def scrape(db, after=None):
    p = {
        "limit" : LIMIT,
        "t" : T
    }
    if after:
        p["after"] = "t3_" + after

    index = None
    for i, post in enumerate(reddit.get("/top", params=p)):
        if i % 10 == 0:
            print(".", end="", flush=True)
        index = db_add(db, post)
    
    return index


def example():
    """ Example code on how to use the functions in this program.
    """
    db = db_load(DB_FILE)

    SUBREDDIT = input("hi there, whose opinion do you want to know: ")
    query = input("what do you want to ask them: ")
    index = None
    for post in search(query):
        index = db_add(db, post)

    print("The database now consists of", len(db), "posts.")
    db_store(db, DB_FILE, index)


if __name__ == '__main__':
    print("Load database...", end="", flush=True)
    db, index = db_load(DB_FILE)
    print(" Done\t\t\tlatest post =", index)

    while True:
        print("Scraping", end="")
        index = scrape(db, index)
        print(" Saving...", end="", flush=True)
        db_store(db, DB_FILE, index)
        print(" Done\tLatest post =", index)
