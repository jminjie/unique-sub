import praw

from subreddit_analyser import SubredditAnalyser

APP_ID = "1g-m6YOi7_8NyA"
APP_SECRET = "eVgGPheds2e76EAHgRYfwACrt30"

def main():
    reddit = praw.Reddit(user_agent="python-script",
                         client_id=APP_ID,
                         client_secret=APP_SECRET)
    subreddit_analyser = SubredditAnalyser(reddit, 'ukulele')
    u, t = subreddit_analyser.uniqueness()
    print "Unique: {0} Total: {1}".format(len(u), t)

if __name__ == "__main__":
    main()
