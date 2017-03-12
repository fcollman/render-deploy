FROM render:forrest 
MAINTAINER Forrest Collman (forrestc@alleninstitute.org) 

#RUN mv deploy/jetty_base/webapps/render-ws.war deploy/jetty_base/.
COPY jetty-rewrite.xml deploy/jetty_base/etc/jetty-rewrite.xml
COPY root-context.xml deploy/jetty_base/webapps/root-context.xml
COPY logback.xml deploy/jetty_base/resources/logback.xml
COPY logback-access.xml deploy/jetty_base/resources/logback.xml
#COPY web.xml /var/www/render/deploy/jetty_base/webapps/web.xml
RUN sed -ie 's\servers=localhost\servers=mongo\g' $JETTY_BASE/logs/render-db.properties
RUN sed -ie 's\#port=27022\port=27017\g' $JETTY_BASE/logs/render-db.properties

#enable re-write module
RUN echo --module=rewrite>>/var/www/render/deploy/jetty_base/start.ini
#RUN ln -sf /dev/stdout /var/log/jetty_bootstrap.log
