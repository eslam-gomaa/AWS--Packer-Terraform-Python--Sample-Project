#!/bin/bash -e
# -e     >> return exit-code 1 if any error occurred

sudo yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
sudo yum repolist
sudo dnf install ansible -y

