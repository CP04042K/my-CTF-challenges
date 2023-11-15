#!/bin/bash

if [[ -z "$(which docker)" ]]
then
    echo "docker is needed, install docker please"
else
    docker build -t freeexe .
    docker run -p3000:3000 freeexe
fi