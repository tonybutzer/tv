#! /bin/bash

# sudo apt update
# sudo apt upgrade

#PREREQUISITES
# sudo apt-get install curl apt-transport-https ca-certificates software-properties-common

# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"


 293  sudo apt update
  294  apt-cache policy docker-ce
  295  sudo apt install docker-ce
  296  sudo systemctl status docker
  297  docker-version
  298  docker --version
  299  docker ps
  300  sudo docker run hello-world

