#!/bin/bash 
javac loadtest.java
echo $SECONDS 
java loadtest 127.0.0.1 8081 11 PUT 1000 &
java loadtest 127.0.0.1 8081 12 PUT 1000 &
java loadtest 127.0.0.1 8081 13 PUT 1000 &
java loadtest 127.0.0.1 8081 14 PUT 1000 &
wait $(jobs -p) 
echo $SECONDS
