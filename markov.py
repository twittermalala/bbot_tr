import markovify
import schedule
import time
import random
import tweepy
import config

try:
    import HTMLParser
except ImportError:
    HTMLParser = None

try:
    import html.parser as htmlparser
except ImportError:
    htmlparser = None

hashtags = [
    '#MAGA',
    '#MakeAmericaGreatAgain',
    '#ImWithYou',
    '#AlwaysTrump',
    '#AmericaFirst',
    '#Trump2016',
    '#TrumpPence16',
    '#PresidentTrump'
]

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_key, config.access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def main():
    speeches()
    schedule.every(10).minutes.do(speeches)
    while 1:
        schedule.run_pending()
        time.sleep(1)


def speeches():
    f = open('speeches.txt', 'r')
    text_model = markovify.Text(f.read())
    tweet = text_model.make_short_sentence(100) + ' ' + random.choice(hashtags)
    print('Posting to Twitter...')
    try:
        api.update_status(HTMLParser.HTMLParser().unescape(tweet))
    except ImportError:
        api.update_status(htmlparser.HTMLParser().unescape(tweet))
    f.close()
    print('Tweet you posted: ' + tweet)


if __name__ == '__main__':
    main()
