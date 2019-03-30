""" This program scrapes the top posts of reddit and puts them in a json file.
It supports the other programs in two ways:

1.  the get(postID) function returns the post description and comment bodies of
a given postID

2.  the VECTORS variable stores the additive and multiplicative vectors of the
titles and descriptions of all posts in the database.
"""

import praw
import json
from praw.models import MoreComments
from numpy import array

# config file contains personal information and should be handled with care
import config
from general_easyness import lprint, minput
from prepare_string import prep, additive, multiplicative


DB_FILE = "reddit_db.json"
VA_FILE = "reddit_va.csv"

SUBREDDIT = ""
LIMIT = 100
T = "all"

DB = dict()
INDEX = None
VECTORS = []

reddit = praw.Reddit(client_id=config.client_id, client_secret=config.client_secret,
                     password=config.password, user_agent=config.user_agent,
                     username=config.username)


def search(query):
    """ Return a list of posts from reddit that fit the query.
        You can specify the results by adjusting the global variables:
        SUBREDDIT, LIMIT and T"""
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
    """ The function for formatting a comment so it can fit in the database """
    content = [comment.score, comment.body, []]
    for sub_comment in comment.replies:
        if type(sub_comment) is not MoreComments:
            content[-1].append(format_comment(sub_comment))

    return content


def format_post(post):
    """ The function for formatting a post so it can fit in the json file. """
    content = [post.title, post.subreddit.display_name, post.upvote_ratio,
               post.score, post.selftext, []]

    for comment in post.comments:
        if (type(comment) is not MoreComments) and not comment.stickied:
            content[-1].append(format_comment(comment))

    return post.id, content


def db_add(post):
    key, content = format_post(post)
    DB[key] = content
    return key


def db_load(filename=DB_FILE):
    """
    the database (named 'DB' throughout this file) is a dictionary of postID keys
    mapped with posts:
    DB = {
        postID_0 : post_0,
        postID_1 : post_1,
        ...
        postID_last : post_last
    }

    A post is stored like this:
    [
        title,                 # string
        name_of_subreddit,     # string
        upvote_ratio,          # float
        score,                 # int
        selftext,              # string

        [
            comment_0,
            comment_1,
            ...
            comment_last
        ]
    ]

    Each comment looks like this:
    [
        score,                 # int
        body,                  # string

        [
            subcomment_0,
            subcomment_1,
            ...
            subcomment_last
        ]
    ]
    """

    DB = {}
    INDEX = None

    print("reddit_search.py:\n\tloading database...", end="", flush=True)
    try:
        with open(filename) as f:
            INDEX = f.readline()[:-1]
            if not INDEX:
                INDEX = None
            DB = json.loads(f.readline())
        print("done.")

    except IOError:
        print("\n\tno database found at", DB_FILE)
        INDEX = None

    return DB, INDEX


def db_store(filename=DB_FILE):
    with open(filename, "w") as f:
        if INDEX:
            f.write(INDEX)
        f.write('\n' + json.dumps(DB))

    vectors_store()


def vectors_load(filename=VA_FILE):
    """ VECTORS looks like this:
        [
            [addition vector 0, multiplicative vector 0, postID 0],
            [addition vector 1, multiplicative vector 1, postID 1],
                                    ...
            [addition vector n, multiplicative vector n, postID n]
        ]
    """

    global VECTORS
    VECTORS = []

    print("\tloading the vector array...", end="", flush=True)
    try:
        with open(filename) as f:
            for line in f:
                add_vec, mul_vec, postID = line.split(",")

                add_vec = array([float(n) for n in add_vec.split(' ')])
                mul_vec = array([float(n) for n in mul_vec.split(' ')])
                VECTORS.append((add_vec, mul_vec, postID[:-1]))

    except IOError:
        print("\n\tno vector array found at", VA_FILE,
              "constructing a new one...", end="", flush=True)

        for postID, post in DB.items():
            arr = prep(post[0] + " " + post[4])
            if arr == []:
                continue
            add_vec, mul_vec = additive(arr), multiplicative(arr)
            VECTORS.append((add_vec, mul_vec, postID))

        print("storing...", end="", flush=True)
        vectors_store(filename)

    print("done.")
    return VECTORS


def vectors_store(filename=VA_FILE):
    with open(filename, 'w') as f:
        for add_vec, mul_vec, postID in VECTORS:
            add_str, mul_str = "", ""

            for i, n in enumerate(add_vec):
                add_str += str(n) + " "
                mul_str += str(mul_vec[i]) + " "

            f.write(add_str[:-1] + ',' + mul_str[:-1] + ',' + postID + '\n')


def scrape():
    global INDEX

    p = {
        "limit" : LIMIT,
        "t" : T
    }
    if INDEX:
        p["after"] = "t3_" + INDEX

    for i, post in enumerate(reddit.get("/top", params=p)):
        if i % 10 == 0:
            print(".", end="", flush=True)
        INDEX = db_add(post)

    return INDEX


def get(postID):
    """ return [
            post.text, [comment0.body, ..., comment_last.body],
            post.score, [comment0.score, ..., comment_last.score]
        ]
    """

    post = DB[postID]
    out = [post[0] + post[-2], [], post[-3], []]

    for comment in DB[postID][-1]:
        body, score = comment[1], comment[0]
        out[1].append(body)
        out[3].append(score)

    return out


DB, INDEX = db_load()
if DB:
    VECTORS = vectors_load()
print()

if __name__ == '__main__':

    print("Latest post =", INDEX)

    while True:
        print("Scraping", end="")
        scrape()
        print(" Saving...", end="", flush=True)
        db_store()
        print(" Done\tLatest post =", INDEX)
