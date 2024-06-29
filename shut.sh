#!/bin/bash
# stop the container
 docker stop math-app-api-con
# remove the container
 docker rm math-app-api-con

 echo "container removed, API is unavailable now..."
 echo "Run sudo ./deploy.sh to start the math-api-app-con [container] for using the api..."