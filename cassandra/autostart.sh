docker stack depoly -c docker-compose.yml url
docker service scale url_redis-replica=2
docker service scale url_url-handler=3