docker compose run --rm dockerfiles
docker run --rm -it -e USER_UID=$(id -u) -e USER_GID=$(id -g) -v ./config/config.json:/app/config/config.json -v 
./data/logs:/app/data/logs -v /var/run/docker.sock:/var/run/docker.sock -v ~/.docker/config.json:/root/.docker/config.json ismailbouajaja/dockerfiles