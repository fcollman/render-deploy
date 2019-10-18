FROM continuumio/miniconda:4.6.14
# RUN conda update conda && conda update python
RUN conda update -y conda && conda install python=2.7

#install java
# RUN set -ex && \
#     echo 'deb http://archive.debian.org/debian jessie-backports main' \
#       > /etc/apt/sources.list.d/jessie-backports.list && \

RUN apt-get update -y && \
    apt-get install \
      openjdk-8-jre \
      ca-certificates-java -y &&\
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /shared
COPY . /shared
WORKDIR /shared
RUN apt-get update && \
    apt-get install --no-install-recommends gcc build-essential libgeos-dev imagemagick xvfb nano vim -y &&\
    python install_all_requirements.py &&\
    apt-get remove --purge gcc build-essential libgeos-dev -y && apt-get autoremove -y &&\
    rm -rf /var/lib/apt/lists/*

# add a simple script that can auto-detect the appropriate JAVA_HOME value
# based on whether the JDK or only the JRE is installed
RUN { \
		echo '#!/bin/sh'; \
		echo 'set -e'; \
		echo; \
		echo 'dirname "$(dirname "$(readlink -f "$(which javac || which java)")")"'; \
	} > /usr/local/bin/docker-java-home \
	&& chmod +x /usr/local/bin/docker-java-home

# do some fancy footwork to create a JAVA_HOME that's cross-architecture-safe
RUN ln -svT "/usr/lib/jvm/java-8-openjdk-$(dpkg --print-architecture)" /docker-java-home
ENV JAVA_HOME /docker-java-home

ENV RENDER_CLIENT_SCRIPTS=/shared/render/render-ws-java-client/src/main/scripts

