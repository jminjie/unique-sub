from progress.bar import Bar
import json
import pprint
import requests
import string

SUBREDDIT = "http://www.reddit.com/r/writingprompts"

# Returns true if the the response is an error
def is_error_response(response):
    if response.has_key('error'):
        return True
    else:
        return False
    
def main():
    f = open('comments.txt', 'a')
    subreddit_words = {}
    top_articles = requests.get(SUBREDDIT + '/top/.json')
    top_articles_data = top_articles.json()
    if is_error_response(top_articles_data):
        print("Error in getting top_articles_data")
        return
    # get the top 25 articles
    progress_bar = Bar('Getting comments for top 25 articles:', max=25)
    for article in top_articles_data['data']['children']:
        article_id = article['data']['id']
        comments = requests.get(SUBREDDIT + '/comments/{0}/.json'.format(article_id))
        comments_data = comments.json()
        if is_error_response(comments_data):
            print("Error in getting comments_data for article_id {0}".format(article_id))
            break
        f.write("ARTICLE_ID = {0}".format(article_id) + '\n')
        # get all the comments for that article
        for comment in comments_data['data']['children'][1]:
            comment_body = comment['data']['body']
            f.write(comment_body)
            # count the unique words
            for word in comment_body:
                cleaned_word = word.lower().translate(None, string.punctuation)
                if subreddit_words.has_key(word):
                    subreddit_words[word] += 1
                else:
                    subreddit_words[word] = 1
        progress_bar.next()
    progress_bar.finish()
    f.close()

if __name__ == "__main__":
    main()
