from redis import Redis
from cassandra.cluster import Cluster
from flask import Flask, request, redirect, abort


app = Flask(__name__)
master = Redis(host='redis-primary', port=6379)
slave = Redis(host='redis-replica', port=6379)

cluster = Cluster(['10.128.1.42', '10.128.2.42', '10.128.3.42'])
session = cluster.connect('urlshortener')


@app.route('/', methods=['PUT'])
def save_long_url():
    short_url = request.args.get('short')
    long_url = request.args.get('long')

    if not short_url or not long_url:
        return 'bad request', 400
    
    try:
        master.set(short_url, long_url)
    except Exception:
        pass

    session.execute("INSERT INTO urls (short_url, long_url) VALUES (%s, %s)", (short_url, long_url))
    return '', 200


@app.route('/', methods=['GET'])
def invalid_method():
    return 'bad request', 400


@app.route('/<short_url>', methods=['GET'])
def redirect_url(short_url):
    try:
        long_url = slave.get(short_url)
    except Exception:
        long_url = None

    if not long_url:
        rows = session.execute("SELECT long_url FROM urls WHERE short_url = %s", (short_url,))

        if not rows:
            return 'page not found', 404

        long_url = rows[0].long_url
        try:
            master.set(short_url, long_url)
        except Exception:
            pass

    return redirect(long_url, code=307)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
