from progress.bar import Bar
import praw
import string

APP_ID = "1g-m6YOi7_8NyA"
APP_SECRET = "eVgGPheds2e76EAHgRYfwACrt30"

# Returns true if the the response is an error
def is_error_response(response):
    if response.has_key('error'):
        return True
    else:
        return False
    
def main():
    # TODO: check if submission is already saved locally
    # if it is, then read from the local version instead of sending request
    reddit = praw.Reddit(user_agent="python-script",
                         client_id=APP_ID,
                         client_secret=APP_SECRET)
    unique_words = set()
    total_words = 0
    f = open('comments.txt', 'a')
    # get the top 25 articles
    progress_bar = Bar('Getting comments for top 25 articles:', max=25)
    for submission in reddit.subreddit('writingprompts').hot(limit=25):
        article_id = submission.shortlink
        all_comments = submission.comments.list()
        f.write("ARTICLE_ID = {0}".format(article_id) + '\n')
        for comment in all_comments:
            body = comment.body
            f.write(body)
            # count the unique words and total words
            for word in body:
                cleaned_word = word.lower().translate(None, string.punctuation)
                unique_words.add(word)
                total_words += 1
        progress_bar.next()
    progress_bar.finish()
    f.write("UNIQUE: {0}\nTOTAL: {1}\n".format(len(unique_words), total_words))
    f.close()

if __name__ == "__main__":
    main()
