import markovify
import schedule
import time
import tweepy
import config
import csv

try:
    import HTMLParser
except ImportError:
    HTMLParser = None

try:
    import html.parser as htmlparser
except ImportError:
    htmlparser = None

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_key, config.access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def main():
    post()
    schedule.every(10).minutes.do(post)
    while 1:
        schedule.run_pending()
        time.sleep(1)


def post():
    with open('realDonaldTrump_tweets.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        text = ''
        for row in reader:
            escapes = ''.join([chr(char) for char in range(1, 32)])
            t = str(row).translate(None, escapes)
            t = t.decode('string_escape')
            text += t

    text_model = markovify.Text(text)

    tweet = text_model.make_short_sentence(140)

    print('Posting to Twitter...')
    try:
        api.update_status(HTMLParser.HTMLParser().unescape(tweet))
    except ImportError:
        api.update_status(htmlparser.HTMLParser().unescape(tweet))
    print('Tweet you posted: ' + tweet)


if __name__ == '__main__':
    main()
