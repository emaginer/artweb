# Quick description

This project is a pet project to build a django template application for art/photo galery.

It intends to be simple, modular in the organization of the webpage, and entirely configurable using django admin.


# Build

Dockerfile can be built uing `docker build artweb .` in the root directory


# Run

`docker run` command can be used to run docker with the following environment variables (can be given to `docker run` with `-e` option):
* PGUSER: username to connect to the postgres database
* PGPASSWORD: password to connect to the postgres database with user PGUSER
* PGHOST: host of the postgres database (ensure the postgres port is open)

Also, media folder with all uploaded images can be match with an host folder as such: `-v /docker/media:/home/docker/code/django/artweb/media`

Port 8000 (application), 9191 and 9001 (supervisord)  needs to be mapped

