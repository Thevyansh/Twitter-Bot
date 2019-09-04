import tweepy
import time

CONSUMER_KEY = 'put your consumer/api key here'
CONSUMER_SECRET = 'put your consumer/api secret here'
ACCESS_TOKEN = 'put your access/token key here'
ACCESS_TOKEN_SECRET = 'put your access/token secret here'


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth)
api.mentions_timeline()

FILE_NAME = 'last_seen_id.txt'


def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


def reply_to_tweets():
    print('retrieving and replying to tweets!')
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id,
                                     tweet_mode='extended')
    for tweet in reversed(mentions):
        print(str(tweet.id) + ' - ' + tweet.full_text)
        last_seen_id = tweet.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#testtweet' in tweet.full_text.lower():
            print('Hashtag found...')
            api.update_status('@' + tweet.user.screen_name + 'Hey There! Back to you', tweet.id)


while True:
    reply_to_tweets()
    time.sleep(2)
