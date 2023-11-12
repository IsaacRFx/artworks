#!/bin/bash

cd /home/appuser/app/artworks/

python manage.py migrate
cd tailwind && npm run build:css && cd ..

exec "$@"