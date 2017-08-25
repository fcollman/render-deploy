FROM continuumio/miniconda
RUN apt-get update \
&& apt-get install --no-install-recommends gcc libgeos-dev imagemagick -y \
&& rm -rf /var/lib/apt/lists/*
RUN mkdir -p /shared
COPY . /shared
WORKDIR /shared
RUN python install_all_requirements.py
RUN apt-get remove --purge gcc libgeos-dev && apt-get autoremove
