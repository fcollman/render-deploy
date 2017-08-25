FROM continuumio/miniconda
RUN mkdir -p /usr/local/base-image
COPY . /usr/local/base-image
WORKDIR /usr/local/base-image
RUN apt-get install gcc build-essential libgeos-dev imagemagick -y
RUN python install_all_requirements.py
