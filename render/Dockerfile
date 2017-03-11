FROM render:forrest 
MAINTAINER Forrest Collman (forrestc@alleninstitute.org) 

COPY root-context.xml /var/www/render/deploy/jetty_base/webapps/root-context.xml
RUN sed -ie 's\servers=localhost\servers=mongo\g' $JETTY_BASE/logs/render-db.properties
RUN sed -ie 's\#port=27022\port=27017\g' $JETTY_BASE/logs/render-db.properties

