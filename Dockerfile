FROM ubuntu

ENV VERS=RUNN
ENV TONY=1.1

RUN apt-get update && \
        apt-get install -y vim \
         && apt-get install hdhomerun-config
