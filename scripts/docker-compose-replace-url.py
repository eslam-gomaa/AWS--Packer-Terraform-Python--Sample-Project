#!/usr/bin/python
import sys

# getting the LB dns name as a parameter
LB_URL = sys.argv[1]

# Change the LB dns name
docker_compose_file = open('./docker-compose.yml', 'r')
docker_compose_file_read = docker_compose_file.read()
docker_compose_file_read = docker_compose_file_read.replace('CHANGE_ME', LB_URL)
docker_compose_file = open('./docker-compose.yml', 'w')
docker_compose_file.write(docker_compose_file_read)
