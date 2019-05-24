# FROM ubuntu
FROM python:3.4

# Install packages
RUN apt-get update &&\
  apt-get install -y \
        apt-utils \
        build-essential \
        vim \
        python \
        python-dev \
        python-setuptools \
        nginx \
        supervisor \
        software-properties-common 

RUN pip install -U pip

########################
# DJANGO INSTALLATIONS #
########################
USER root
RUN pip install uwsgi
ADD django/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

##############
# DJANGO APP #
##############
ADD . /home/docker/code
RUN mkdir -p /var/log/django

# # setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /home/docker/code/nginx-app.conf /etc/nginx/sites-enabled/
RUN ln -s /home/docker/code/supervisor-app.conf /etc/supervisor/conf.d/
RUN python /home/docker/code/django/artweb/manage.py collectstatic --noinput

###########
# GENERAL #
###########
WORKDIR /home/docker/code/

# Expose the application port
EXPOSE 8000 9001 9191 

CMD ["supervisord", "-n"]
