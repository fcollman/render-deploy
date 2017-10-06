FROM fcollman/render-ws
USER root
ARG NDVIZHOST=localhost
ARG NDVIZPORT=8000
#RUN mv deploy/jetty_base/webapps/render-ws.war deploy/jetty_base/.
COPY jetty-rewrite.xml $JETTY_BASE/etc/jetty-rewrite.xml
RUN echo $NDVIZHOST:$NDVIZPORT
RUN sed -ie "s/NDVIZHOST/$NDVIZHOST:$NDVIZPORT/g" $JETTY_BASE/etc/jetty-rewrite.xml
COPY root-context.xml $JETTY_BASE/webapps/root-context.xml
COPY logback.xml $JETTY_BASE/resources/logback.xml
COPY render-db.properties $JETTY_BASE/logs/render-db.properties

ENV JAVA_OPTIONS="-Xms2g -Xmx2g -server -Djava.awt.headless=true"
#enable re-write module
RUN echo --module=rewrite>>$JETTY_BASE/start.d/start.ini
USER jetty
#RUN echo --ndvizHost=$HOSTNAME:8889>>/var/www/render/deploy/jetty_base/start.ini
#RUN ln -sf /dev/stdout /var/log/jetty_bootstrap.log
