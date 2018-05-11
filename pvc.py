import os
import redis
import twitter

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

POLL_MAX_ID = 'POLL_MAX_ID'

# These should be in a db and they are used as our #hashtags
POLL_KEY_YES = '#PVCTESTYES'
POLL_KEY_NO = '#PVCTESTNO'
#POLL_KEY_YES = '#YesYouCan'
#POLL_KEY_NO = '#BEEMERGENCYREADY'

TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
TWITTER_TOKEN_KEY = os.environ.get('TWITTER_TOKEN_KEY')
TWITTER_TOKEN_SECRET = os.environ.get('TWITTER_TOKEN_SECRET')

db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def get_max_id(hash_tag):
    '''Get from redis'''
    key = '{}-MAXID'.format(hash_tag)
    return db.get(key) or 1


def set_max_id(hash_tag, max_id):
    '''Set in redis'''
    key = '{}-MAXID'.format(hash_tag)
    db.set(key, max_id)


def get_tweets(hash_tag, invalid, count=5, max_id=0):
    max_id = get_max_id(hash_tag)

    api = twitter.Api(
        consumer_key=TWITTER_CONSUMER_KEY,
        consumer_secret=TWITTER_CONSUMER_SECRET,
        access_token_key=TWITTER_TOKEN_KEY,
        access_token_secret=TWITTER_TOKEN_SECRET)

    res = api.GetSearch(
        term=hash_tag,
        since_id=max_id,
        count=count,
        return_json=True)

    set_max_id(hash_tag, res['search_metadata']['max_id'])

    for row in res['statuses']:
        print(row['user']['screen_name'])
        db.sadd(hash_tag, row['user']['screen_name'])
        db.srem(invalid, row['user']['screen_name'])


if __name__ == '__main__':
    # print(POLL_KEY_YES)
    new_max = get_tweets(POLL_KEY_YES, POLL_KEY_NO, 5)
    # print(POLL_KEY_NO)
    new_max = get_tweets(POLL_KEY_NO, POLL_KEY_YES, 5)
