import redis
from cassandra.cluster import Cluster

master = redis.Redis(host='redis-primary', port=6379)
slave = redis.Redis(host='redis-replica', port=6379)

try:
    cluster = Cluster(['10.128.1.42', '10.128.2.42', '10.128.3.42'])
    session = cluster.connect('urlshortener')
except Exception:
    session = None

stream_name = 'url_stream'
group_name = 'url_group'

master.xgroup_create(stream_name, group_name, id='0', mkstream=True)


def process_messages():
    while True:
        try:
            messages = master.xreadgroup(group_name, 'consumer', {stream_name: '>'}, count=5, block=1000)
            for message in messages:
                msg_id, data = message
                short_url = data['short_url']
                long_url = data['long_url']

                session.execute("INSERT INTO urls (short_url, long_url) VALUES (%s, %s)", (short_url, long_url))
                master.xack(stream_name, group_name, msg_id)
        except Exception:
            pass


if __name__ == '__main__':
    process_messages()
