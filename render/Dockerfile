FROM render:forrest 
MAINTAINER Forrest Collman (forrestc@alleninstitute.org) 

RUN mv deploy/jetty_base/webapps/render-ws.war deploy/jetty_base/.
COPY root-context.xml /var/www/render/deploy/jetty_base/webapps/root-context.xml
COPY web.xml /var/www/render/deploy/jetty_base/webapps/web.xml
RUN sed -ie 's\servers=localhost\servers=mongo\g' $JETTY_BASE/logs/render-db.properties
RUN sed -ie 's\#port=27022\port=27017\g' $JETTY_BASE/logs/render-db.properties

#enable re-write module
RUN echo OPTION=rewrite>>/var/www/render/deploy/jetty_base/start.ini
