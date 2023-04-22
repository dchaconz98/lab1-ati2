#!/bin/bash

python -m venv .venv
mkdir ./.cache
source .venv/bin/activate && pip install --cache-dir ./.cache -r requirements/local.txt && python manage.py migrate && python manage.py createsuperuser
