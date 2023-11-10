docker service rm $(docker service ls -q)
docker stack deploy -c fast-url-handler.yml url
