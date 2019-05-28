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
ARG SECRET_KEY
ENV SECRET_KEY=$SECRET_KEY
ARG PGUSER
ENV PGUSER=$PGUSER
ARG PGPASSWORD
ENV PGPASSWORD=$PGPASSWORD
ARG PGHOST
ENV PGHOST=$PGHOST
ARG PGPORT
ENV PGPORT=$PGPORT
ARG ALLOWED_HOSTS
ENV ALLOWED_HOSTS=$ALLOWED_HOSTS

ARG AWS_S3_ENDPOINT_URL
ENV AWS_S3_ENDPOINT_URL=$AWS_S3_ENDPOINT_URL
ARG AWS_S3_REGION_NAME
ENV AWS_S3_REGION_NAME=$AWS_S3_REGION_NAME
ARG AWS_SECRET_ACCESS_KEY
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ARG AWS_ACCESS_KEY_ID
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ARG AWS_STORAGE_BUCKET_NAME
ENV AWS_STORAGE_BUCKET_NAME=$AWS_STORAGE_BUCKET_NAME
ARG AWS_S3_HOST
ENV AWS_S3_HOST=$AWS_S3_HOST


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
