#!/usr/bin/env bash
# exit on error
set -o errexit

#poetry install
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

export LC_ALL="es_ES.UTF-8"
export LC_CTYPE="es_ES.UTF-8"
sudo dpkg-reconfigure locales