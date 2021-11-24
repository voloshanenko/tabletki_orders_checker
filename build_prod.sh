#! /bin/bash
source env.prod
docker build -t tabletki_orders_checker .
docker tag tabletki_orders_checker ${DOCKER_REGISTRY}/tabletki_orders_checker:latest
docker push ${DOCKER_REGISTRY}/tabletki_orders_checker:latest
python deploy/deploy.py
