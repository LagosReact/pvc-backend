import os
import redis
from flask import Flask, request, jsonify


app = Flask(__name__)

REDIS_HOST = os.environ.get('REDIS_HOST', '')
REDIS_PORT = os.environ.get('REDIS_PORT', '')

db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


@app.route('/')
def search_db():
    redis_key = request.args.get('key', '')
    if not redis_key:
        return jsonify({'message': 'go away jare'})
    else:
        yes_key = '#{}YES'.format(redis_key).upper()
        no_key = '#{}NO'.format(redis_key).upper()

        yes_count = db.scard(yes_key)
        no_count = db.scard(no_key)

        return jsonify({'yes': yes_count, 'no': no_count, 'key': redis_key})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
