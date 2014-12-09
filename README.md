##uni-website

An example website using Flask, Python3 and Postgresql.

This example consists of two apps: one is a regular site with home and about page,
and the other one is an exam. You need to login to take the exam.

###Usage

You need to create a postgresql database before running this app.
The `db_create.py` file and `data` directory provide examples of how to
populate the database.

The `setup_website.sh` script is for use with Ubuntu and can be used
to setup this app with Flask, Postgresql and Apache.

###Customizing this app

The exam app was written for an English exam with reading, listening
and writing sections, as can be seen if you look at the `questions.html`
template in the `templates` directory. However, it is also meant to be
easily customizable. If you have any questions about customization,
feel free to let me know.

####License

GPLv3.
