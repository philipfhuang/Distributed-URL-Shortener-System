from flask import Flask, request, redirect
import redis
import cassandra

app = Flask(__name__)
r = redis.Redis()


@app.route('/')
def save_long_url(long_url):
    short_url = request.args.get('short')
    long_url = request.args.get('long')
    r.set(short_url, long_url)
    # TODO: Should we save in Cassandra right now or later?

    return


@app.route('/<short_url>', methods=['GET'])
def redirect_url(short_url):
    long_url = r.get(short_url)

    # TODO: Find in Cassandra if not in Redis
    if not long_url:
        pass

    return redirect(long_url, code=307)


if __name__ == '__main__':
    app.run()
