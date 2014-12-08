#!/bin/bash
# simple script to get this app running with Apache on Ubuntu 14.04

sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get -y install apache2 libapache2-mod-wsgi-py3
sudo a2enmod wsgi
sudo apt-get -y install python3-dev python3-pip python3-software-properties software-properties-common \
    postgresql-9.3 postgresql-server-dev-9.3
sudo /etc/init.d/postgresql start &&\
    sudo -u postgres psql -c "CREATE USER comein WITH PASSWORD 'comein' CREATEDB;" &&\
    sudo -u postgres psql -c "CREATE DATABASE comein WITH OWNER comein"
sudo pip3 install Flask Flask-Login Flask-SQLAlchemy Flask-WTF Jinja2 SQLAlchemy\
    WTForms Werkzeug itsdangerous psycopg2 passlib
python3 db_create.py
sudo cp uni_web.conf /etc/apache2/sites-available/
sudo cp -r /home/$USER/uni_web /var/www/uni_web
sudo chown -R www-data:www-data /var/www/uni_web
sudo a2ensite uni_web
sudo a2dissite 000-default
sudo service apache2 restart
