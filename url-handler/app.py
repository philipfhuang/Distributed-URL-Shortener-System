from redis import Redis
from cassandra.cluster import Cluster
from flask import Flask, request, redirect


app = Flask(__name__)
master = Redis(host='redis-primary', port=6379)
slave = Redis(host='redis-replica', port=6379)

# TODO: Need to change the IP address to the IP address of the Cassandra container
cluster = Cluster(['127.0.0.1'])
# TODO: Need to change the keyspace to the keyspace of the Cassandra container
session = cluster.connect('urlshortener')


@app.route('/')
def save_long_url(long_url):
    short_url = request.args.get('short')
    long_url = request.args.get('long')
    master.set(short_url, long_url)
    session.execute("INSERT INTO urls (short_url, long_url) VALUES (%s, %s)", (short_url, long_url))
    return 'OK'


@app.route('/<short_url>', methods=['GET'])
def redirect_url(short_url):
    long_url = slave.get(short_url)

    if not long_url:
        rows = session.execute("SELECT long_url FROM urls WHERE short_url = %s", (short_url,))
        long_url = rows.long_url
        master.set(short_url, long_url)

    return redirect(long_url, code=307)


if __name__ == '__main__':
    app.run()