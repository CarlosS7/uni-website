##uni-website

An example website using Flask, Python3 and Postgresql.

This example consists of two apps: one is a regular site with home and about page,
and the other one is an exam. You need to login to take the exam.

###Usage

You need to create a postgresql database before running this app.
The `db_create.py` file and `data` directory provide examples of how to populate
the database.

The `setup_website.sh` script is for use with Ubuntu and can be used
to setup this app with Flask, Postgresql and Apache.
