#!/bin/bash
for i in {1..100}
do
  short_url="short$i"
  long_url="http://www.example$i.com/"
  
  curl -X PUT "http://localhost:8081/?short=$short_url&long=$long_url"
  curl -X GET "http://localhost:8081/$short_url"
done
