#!/usr/bin/python
import praw
from subreddit_analyser import SubredditAnalyser

APP_ID = "1g-m6YOi7_8NyA"
APP_SECRET = "eVgGPheds2e76EAHgRYfwACrt30"

def main():
    reddit = praw.Reddit(user_agent="python-script",
                         client_id=APP_ID,
                         client_secret=APP_SECRET)
    subreddits = []
    #subreddits.append('ukulele')
    #subreddits.append('calvinandhobbes')
    #subreddits.append('nekoatsume')
    subreddits.append('askreddit')
    subreddits.append('politics')

    for subreddit in subreddits:
        subreddit_analyser = SubredditAnalyser(reddit, subreddit)
        u, t = subreddit_analyser.uniqueness()
        print "{0} Unique: {1} Total: {2}".format(subreddit, len(u), t)

if __name__ == "__main__":
    main()
