#!/bin/bash
BUILD_FLAG=false
WORKDIR=$(pwd)
NAME=skyscraper:latest

# Build image and delete old versiones
if $BUILD_FLAG ; then
	echo "=> Building image..."
	docker build $WORKDIR --pull --no-cache --rm --tag $NAME
	docker rmi `docker images | grep "<none>" | awk {'print $3'}`
	echo "=> Image $NAME built"
else
	echo "=> Image $NAME already built"
fi

# Run docker container
docker run -itd --rm -p 8080:8080 \
            --mount type=bind,source=$WORKDIR/src,target=/home/skyscraper \
            $NAME > /dev/null

CONTAINER_ID=`docker ps | grep $NAME | awk {'print $NF'}`
echo "=> Container $CONTAINER_ID ($NAME) running..."

# Execute commands in container
echo "=> Executing commands in container..."
echo "*************************************"
docker exec -it $CONTAINER_ID /bin/sh -c "python3 /home/skyscraper/sky.py"
echo "*************************************"
echo "=> Commands execution finished"
# Stop container and exit
docker stop $CONTAINER_ID > /dev/null
echo "=> Container $CONTAINER_ID stopped"
echo "=> Execution finished"