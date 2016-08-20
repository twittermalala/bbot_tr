import sys
import markovify
import schedule
import time
import random
from Tweets import Tweets

hashtags = ['#MAGA', '#MakeAmericaGreatAgain', '#ImWithYou', '#AlwaysTrump', '#AmericaFirst']
tweets = Tweets()


def main(args):
    read = ''

    print 'Trump Markov Chain'
    print('Enter ? for a list of valid commands.')

    while read != 'exit':
        read = raw_input()

        if read == '?':
            print("Enter 'seed' to to retrieve tweets and store in the database.")
            print("Enter 'speeches' to load the text model from the speeches.txt file.")
            print("Enter 'bot' to retrieve tweets from your database and post to Twitter.")
            print("Enter 'exit' to close the program")

        if read == 'seed':
            seed()

        if read == 'speeches':
            speeches()
            schedule.every(10).minutes.do(speeches)
            while 1:
                schedule.run_pending()
                time.sleep(1)

        if read == 'exit':
            pass

        if read == 'bot':
            bot()
            schedule.every(10).minutes.do(bot)
            while 1:
                schedule.run_pending()
                time.sleep(1)


def seed():
    try:
        user = raw_input('Enter the twitter handle: \n')
    except NameError:
        user = input('Enter the twitter handle: \n')
    print('Getting tweets for ' + user + '. This may take a while.')
    t = Tweets()
    t.set_screen_name(user)
    new_tweets = t.new_tweets()
    print('Inserting into Database')
    t.insert(new_tweets)
    print('Database created')


def speeches():
    f = open('speeches.txt', 'r')
    text_model = markovify.Text(f.read())
    tweet = text_model.make_sentence() + ' ' + random.choice(hashtags)
    print('Posting to Twitter...')
    shorten = (tweet[:140]) if len(tweet) > 140 else tweet
    tweets.post(shorten)
    f.close()
    print('Tweet you posted: ' + tweet)


def bot():
    print('Getting tweets from database...')
    all_tweets = tweets.all_tweets()
    print('Generating tweet')
    text_model = ''
    for d in all_tweets:
        text_model += " "
        text_model += d['text']
    text_model = markovify.Text(text_model)
    tweet = text_model.make_sentence() + ' ' + random.choice(hashtags)
    print('Posting to Twitter...')
    shorten = (tweet[:140]) if len(tweet) > 140 else tweet
    tweets.post(shorten)
    print('Tweet you posted: ' + tweet)


if __name__ == '__main__':
    main(sys.argv[1:])
