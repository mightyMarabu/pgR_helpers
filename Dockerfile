FROM postgres:10
#MAINTAINER Sebastian Schmidt

ENV PGROUTING_MAJOR 2.5
ENV PGROUTING_VERSION 2.5.2

ENV POSTGIS_MAJOR 2.5
ENV POSTGIS_VERSION 2.5.1+dfsg-1.pgdg90+1

#ENV PLPYTHON_VERSION 10.6-1.pgdg18.04+1

# python extension
RUN apt-get update \
      && apt-get install -y --no-install-recommends \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR=$POSTGIS_VERSION \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR-scripts=$POSTGIS_VERSION \
           postgis=$POSTGIS_VERSION \
           python3 postgresql-plpython3-$PG_MAJOR \
           python3-requests python3-numpy \
      wget \
      postgresql-$PG_MAJOR-pgrouting && \
    rm -rf /var/lib/apt/lists/*

#OSM_fdw
RUN pgxn install osm_fdw   

#RUN mkdir -p /docker-entrypoint-initdb.d/
#COPY ./initdb-pgrouting.sh /docker-entrypoint-initdb.d/routing.sh
