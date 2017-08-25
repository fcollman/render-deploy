FROM continuumio/miniconda
RUN mkdir -p /usr/local/base-image
COPY . /usr/local/base-image
WORKDIR /usr/local/base-image
RUN apt-get update \
&& apt-get install gcc libgeos-dev imagemagick -y \
&& rm -rf /var/lib/apt/lists/*
RUN python install_all_requirements.py
