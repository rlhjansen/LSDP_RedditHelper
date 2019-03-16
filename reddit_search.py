import praw

# config file contains personal information and should be handled with care
import config
from general_easiness lprint, minput


secret = "QZkg5lKfPvGXg0i8TFX97QsP_Sk"
id = "e_X0O6AgPqeOOg"
reddit = praw.Reddit(client_id=config.client_id, client_secret=config.client_secret,
                     password=config.password, user_agent=config.user_agent,
                     username=config.username)

# reddit.subreddit('test').submit('Test Submission', url='https://reddit.com')


submission = reddit.submission(url='https://www.reddit.com/r/funny/comments/3g1jfi/buttons/')
print(submission.comments)
