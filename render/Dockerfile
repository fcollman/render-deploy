FROM render:forrest 
MAINTAINER Forrest Collman (forrestc@alleninstitute.org) 

RUN sed -ie 's\servers=localhost\servers=mongo\g' $JETTY_BASE/logs/render-db.properties
RUN sed -ie 's\#port=27022\port=27017\g' $JETTY_BASE/logs/render-db.properties
RUN mkdir -p /nas
RUN mkdir -p /nas2

