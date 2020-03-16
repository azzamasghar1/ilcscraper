#!/bin/bash
set -e

echo "Starting SSH ..."
service ssh start

echo "Starting Python flask server ..."
#python application.py runserver 0.0.0.0:8000
flask run --host 0.0.0.0 --port=8000