import praw
import json
from praw.models import MoreComments

# config file contains personal information and should be handled with care
import config
from general_easyness import lprint, minput


DB_FILE = "reddit_db.json"

SUBREDDIT = ""
LIMIT = 99
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
        content[-1].append(format_comment(sub_comment))
    return content


def format_post(post):
    content = [post.title, post.subreddit.display_name, post.upvote_ratio,
               post.score, post.selftext, []]

    for comment in post.comments:
        if comment.stickied:
            continue

        content[-1].append(format_comment(comment))

    return post.id, content


def db_add(db, posts):
    for post in posts:
        key, content = format_post(post)
        db[key] = content
    return db


def db_load(filename):
    db = None
    try:
        with open(filename) as f:
            db = json.loads(f.read())
    except IOError:
        db = {}
    return db


def db_store(db, filename):
    with open(filename, "w") as f:
        f.write(json.dumps(db))


if __name__ == '__main__':
    db = db_load(DB_FILE)

    SUBREDDIT = input("hi there, whose opinion do you want to know: ")
    query = input("what do you want to ask them: ")
    db_add(db, search(query)[:2])

    print("The size of the database is:", len(db))

    db_store(db, DB_FILE)

    """

    for i in search(query)[:3]:
        print("\t", i.title)
        print(i.selftext)
        print("Comment")
        print(i.comments[0].body)
        print()
    """