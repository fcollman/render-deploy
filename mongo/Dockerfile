#
# MongoDB Dockerfile
#
# https://github.com/dockerfile/mongodb
#

# Pull base image.
FROM ubuntu:16.04

# Install MongoDB.
RUN \
  apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10 && \
  echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' > /etc/apt/sources.list.d/mongodb.list && \
  apt-get update && \
  apt-get install -y mongodb-org && \
  apt-get install -y numactl && \
  rm -rf /var/lib/apt/lists/*

ENV MONGO_USER=mongodb \
    MONGO_DATA_DIR=/data/db \
    MONGO_LOG_DIR=/var/log/mongodb

RUN sed 's/^bind_ip/#bind_ip/' -i /etc/mongod.conf 
EXPOSE 27017/tcp
VOLUME ["${MONGO_DATA_DIR}"]
CMD ["/usr/bin/mongod"]
