FROM continuumio/miniconda
RUN mkdir -p /usr/local/render-shared
COPY . /usr/local/render-shared
WORKDIR /usr/local/render-shared
RUN python install_all_requirements.py
