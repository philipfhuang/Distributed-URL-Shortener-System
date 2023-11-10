#!/bin/bash 
javac loadtest.java
echo $SECONDS 
java loadtest 127.0.0.1 8081 11 GET 1000 &
java loadtest 127.0.0.1 8081 11 GET 1000 &
java loadtest 127.0.0.1 8081 11 GET 1000 &
java loadtest 127.0.0.1 8081 12 GET 1000 &
wait $(jobs -p) 
echo $SECONDS
