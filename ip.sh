#!/bin/bash

echo -n "devserver: "
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' paypwn-devserver-1

echo -n "nginx:     "
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' paypwn-nginx-1
