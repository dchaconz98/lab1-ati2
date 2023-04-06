#!/bin/bash
#pushd ..
source dev.sh
docker-compose stop django
dockerpy python setup_dev.py --reset-db
docker-compose start django
