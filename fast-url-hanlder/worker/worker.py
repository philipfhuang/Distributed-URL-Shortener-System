import redis
import socket
from cassandra.cluster import Cluster

hostname = socket.gethostname()
master = redis.Redis(host='redis-primary', port=6379)
slave = redis.Redis(host='redis-replica', port=6379)

try:
    cluster = Cluster(['10.128.1.42', '10.128.2.42', '10.128.3.42'])
    session = cluster.connect('urlshortener')
except Exception:
    session = None

stream_name = 'url_stream'
group_name = 'url_group'

try:
    master.xgroup_create(stream_name, group_name, id='0', mkstream=True)
except redis.exceptions.ResponseError as e:
    if "BUSYGROUP Consumer Group name already exists" in str(e):
        print("Consumer group already exists.")
    else:
        raise e


def process_messages():
    counter = 0
    while True:
        try:
            messages = master.xreadgroup(group_name, hostname, {stream_name: '>'}, count=100, block=0)
            for message in messages:
                msg_id, data = message
                print(message)
                short_url = data['short_url']
                long_url = data['long_url']

                session.execute("INSERT INTO urls (short_url, long_url) VALUES (%s, %s)", (short_url, long_url))
                master.xack(stream_name, group_name, msg_id)

                counter += 1
                print(f"msg: {message} counter: {counter}")
        except Exception as e:
            print(e)
        print("counter: ", counter)


if __name__ == '__main__':
    process_messages()
