#!/bin/bash

docker run --rm -it -p 15672:15672 -p 5672:5672 rabbitmq:management
