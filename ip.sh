#!/bin/bash

docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' paypwn-devserver-1
#docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' paypwn-nginx-1
