basepath := $(shell pwd)

network:
	docker network create -d overlay --attachable spider

spider-nginx:
	docker service create --name spider_nginx \
--constraint node.role==manager \
-p 6379:6379 \
--mount type=bind,source=$(basepath)/nginx/nginx-base.conf,target=/etc/nginx/nginx.conf \
--mount type=bind,source=$(basepath)/nginx/nginx-stream-proxy.conf,target=/etc/nginx/stream.conf.d/nginx-stream-proxy.conf \
--mount type=bind,source=$(basepath)/nginx/nginx-http-proxy.conf,target=/etc/nginx/conf.d/default.conf \
--network spider nginx:alpine

spider:
	docker stack deploy -c docker-compose.yml spider

build:
	docker build -t "inner.registry:5000/spider" .

push:
	docker push "inner.registry:5000/spider"
