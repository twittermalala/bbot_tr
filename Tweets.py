import tweepy
import config
import re
from Database import Database
import sys
import pymysql.cursors

try:
    import HTMLParser
except ImportError:
    HTMLParser = None

try:
    import html.parser as htmlparser
except ImportError:
    htmlparser = None


class Tweets:
    def __init__(self):
        self.screen_name = ''
        self.auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
        self.auth.set_access_token(config.access_key, config.access_secret)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.conn = Database().conn

    def set_screen_name(self, screen_name):
        self.screen_name = screen_name

    def post(self, tweet):
        try:
            self.api.update_status(HTMLParser.HTMLParser().unescape(tweet))
        except ImportError:
            self.api.update_status(htmlparser.HTMLParser().unescape(tweet))
            

    def insert(self, tweets):
        for tweet in tweets:
            with self.conn.cursor() as cursor:

                try:

                    # Remove URLS and @ mentions
                    text = re.sub(r"(?:\@|https?\://)\S+", "", tweet.text)

                    # Remove double and single quotes
                    string = text.replace('"', '').replace("'", '')

                    # Remove additional spaces
                    string = ' '.join(string.split())

                    sql = "INSERT INTO `tweets` (`text`, `twitter_id`) VALUES (%s, %s)"
                    cursor.execute(sql, (string, tweet.id))
                    self.conn.commit()
                except pymysql.err.InternalError as p:
                    print(p.message)
                    continue

    def all_tweets(self):
        with self.conn.cursor() as cursor:
            sql = "SELECT text FROM tweets"
            cursor.execute(sql)
            return cursor.fetchall()

    def new_tweets(self):
        if self.screen_name == '':
            sys.exit()
        else:
            all_tweets = []
            new_tweets = self.api.user_timeline(screen_name=self.screen_name, count=1, include_rts=False)
            all_tweets.extend(new_tweets)
            oldest = all_tweets[-1].id - 1
            while len(new_tweets) > 0:
                new_tweets = self.api.user_timeline(screen_name=self.screen_name, count=200, max_id=oldest,
                                                    include_rts=False)
                all_tweets.extend(new_tweets)
                oldest = all_tweets[-1].id - 1

            return all_tweets
