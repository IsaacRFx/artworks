#!/bin/bash

cd /home/appuser/app/artworks/

python manage.py migrate

exec "$@"