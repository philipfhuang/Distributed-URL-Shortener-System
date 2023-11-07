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

try:
    master.xgroup_create(stream_name, group_name, id='0', mkstream=True)
except redis.exceptions.ResponseError as e:
    if "BUSYGROUP Consumer Group name already exists" in str(e):
        print("Consumer group already exists.")
    else:
        raise e

