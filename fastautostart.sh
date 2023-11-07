docker service rm $(docker service ls -q)
docker stack deploy -c fast-url-handler.yml url
docker service scale url_redis-replica=2
docker service scale url_worker=3
docker service scale url_fast-handler=3
