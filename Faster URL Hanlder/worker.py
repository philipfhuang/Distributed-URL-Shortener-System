from cassandra.cluster import Cluster

cluster = Cluster(['10.128.1.42', '10.128.2.42', '10.128.3.42'])
try:
    session = cluster.connect('urlshortener')
except Exception:
    session = None

stream_name = 'url_stream'
group_name = 'url_group'

