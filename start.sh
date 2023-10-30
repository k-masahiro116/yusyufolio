#!/bin/sh
source myvenv/bin/activate
cd my_portfolio
# python3 manage.py runserver 8080
python3 manage.py runserver 0.0.0.0:8080
