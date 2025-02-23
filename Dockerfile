FROM postgres:16-bullseye

ENV PG_MAJOR 16
ENV POSTGIS_MAJOR 3

RUN apt-get update
RUN apt-get install -y postgis postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

RUN mkdir -p /docker-entrypoint-initdb.d
COPY ./initdb-postgis.sh /docker-entrypoint-initdb.d/10_postgis.sh