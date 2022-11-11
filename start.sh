#!/usr/bin/env bash

image_name='jasome-serving'
container_name='jasome-ai-container'

if [ $# -eq 1 ]; then
  if ! [ "$(git log --pretty=%H ...refs/heads/master^ | head -n 1)" = "$(git ls-remote origin -h refs/heads/master | cut -f1)" ]; then
    # need pull and rebuild image
    git pull origin master
    docker build -t $image_name .
  fi
  if [ "$(docker ps -aq -f name=$container_name)" ]; then
    # cleanup
    docker rm $container_name
  fi
  # run your container
  docker run -it -v "$1":/app/models -p 5000:5000 --name $container_name $image_name
else
  echo "모델이 위치한 디렉터리의 절대 경로를 입력해주세요."
fi
