import praw
from praw.models import MoreComments

# config file contains personal information and should be handled with care
import config
from general_easyness import lprint, minput


reddit = praw.Reddit(client_id=config.client_id, client_secret=config.client_secret,
                     password=config.password, user_agent=config.user_agent,
                     username=config.username)

# reddit.subreddit('test').submit('Test Submission', url='https://reddit.com')


# cars = praw.models.Subreddit(reddit, display_name="JordanPeterson")
# for i in cars.search("zizek", limit=5):
#     print(i.title)
#


if __name__ == '__main__':
    if True:
        subreddit = input("hi there, whose opinion do you want to know?\n")
        # check if subreddit exists
        query = input("what do you want to ask them\n")
    else:
        subreddit = "chapoTrapHouse"
        query = "who is yang"
    subreddit_inst = praw.models.Subreddit(reddit, display_name=subreddit)
    for i in subreddit_inst.search(query, limit=1):
        # print("Title:", i.title)
        # print("body", i.selftext)
        # print()
        print(i.comments[0].body)
        # print()
        query = input("anything else you want to ask?")
    while query != "no":
        for i in subreddit_inst.search(query, limit=1):
            # print("Title:", i.title)
            # print("body", i.selftext)
            # print()
            if query == "where":
                print(subreddit)
            else:
                print(i.comments[0].body)
            # print()
        query = input("anything else you want to ask?")

# submission = reddit.submission(url='https://www.reddit.com/r/funny/comments/3g1jfi/buttons/')
# lprint([elem.body for elem in submission.comments if not isinstance(elem, MoreComments)])
