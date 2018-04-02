#!/bin/bash

cd /root/messenger/frontend

if [ ! -d node_modules ]; 
    then npm install
fi

cd ../backend

pip3 install -r /tmp/requirements.txt

python3 manage.py makemigrations --noinput

python3 manage.py migrate --noinput

python3 manage.py collectstatic --noinput

env > /etc/environment

supervisord -n