from progress.bar import Bar
import praw
import string

APP_ID = "1g-m6YOi7_8NyA"
APP_SECRET = "eVgGPheds2e76EAHgRYfwACrt30"

def load_stopwords():
    stopwords= []
    f = open('stopwords.txt', 'r')
    for line in f:
        stopwords.append(line.strip())
    f.close()
    return stopwords

class SubredditAnalyser:
    def is_url(self, word):
        return "http" in word

    def is_stopword(self, word):
        return word in self.stopwords

    # word is probably something like 'TOPKEKTOPKEKTOPKEKTOPKEKTOPKEKTOPKEKT...'
    def is_wall(self, word):
        return len(word) > 30

    def uniqueness(self, num_articles=25):
        # TODO: check if submission is already saved locally
        # if it is, then read from the local version instead of sending request
        unique_words = set()
        total_words = 0
        self.stopwords = load_stopwords()
        f = open('data_{}.txt'.format(self.subreddit), 'a')
        # get the top 25 articles
        progress_bar = Bar('Getting comments for articles in /r/{0}:'
                .format(self.subreddit), max=num_articles)
        for submission in self.reddit.subreddit(self.subreddit).hot(limit=
                num_articles):
            article_id = submission.shortlink
            # resolve MoreComments instances
            submission.comments.replace_more(limit=None)
            all_comments = submission.comments.list()
            f.write("ARTICLE_ID = {0}".format(article_id) + '\n')
            for comment in all_comments:
                
                body = comment.body.encode('utf-8')
                f.write(body + '\n')
                # count the unique words and total words
                words = body.split()
                for word in words:
                    cleaned_word = str(word.lower()).translate(None,
                            string.punctuation)
                    if self.is_url(cleaned_word) or self.is_stopword(cleaned_word)
                            or self.is_wall(cleaned_word):
                        continue
                    unique_words.add(cleaned_word)
                    total_words += 1
            progress_bar.next()
        progress_bar.finish()
        f.write(str(unique_words) + '\n')
        f.write("UNIQUE: {0}\nTOTAL: {1}\n".format(len(unique_words), total_words))
        f.close()
        return unique_words, total_words

    def __init__(self, reddit_instance, subreddit, custom_stopwords=None):
        self.reddit = reddit_instance
        self.subreddit = subreddit
        if custom_stopwords is None:
            self.stopwords = load_stopwords()
        else:
            self.stopwords = custom_stopwords

