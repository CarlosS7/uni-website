#!/bin/bash

sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install libapache2-mod-wsgi
sudo a2enmod wsgi
sudo apt-get install -y python3-dev python3-pip python3-software-properties software-properties-common \
    postgresql-9.3 postgresql-client-9.3 postgresql-contrib-9.3
sudo /etc/init.d/postgresql start &&\
    sudo -u postgres psql -c "CREATE USER comein WITH PASSWORD 'comein' CREATEDB;" &&\
    sudo -u postgres psql -c "CREATE DATABASE comein WITH OWNER comein"
sudo pip3 install Flask Flask-Login Flask-SQLAlchemy Flask-WTF Jinja2 SQLAlchemy\
    WTForms Werkzeug itsdangerous psycopg2 passlib
python3 db_create.py
sudo cp uni_web.conf /etc/apache2/sites-available/
sudo a2ensite uni_web
sudo service apache2 restart
