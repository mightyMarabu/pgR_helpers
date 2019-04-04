FROM postgres:10
#MAINTAINER Sebastian Schmidt

ENV PGROUTING_MAJOR 2.5
ENV PGROUTING_VERSION 2.5.2

ENV POSTGIS_MAJOR 2.5
ENV POSTGIS_VERSION 2.5.1+dfsg-1.pgdg90+1

ENV BUILD_TOOLS="cmake make gcc libtool git pgxnclient postgresql-server-dev-$PG_MAJOR"

#ENV PLPYTHON_VERSION 10.6-1.pgdg18.04+1

# python extension
RUN apt-get update \
      && apt-get install -y --no-install-recommends \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR=$POSTGIS_VERSION \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR-scripts=$POSTGIS_VERSION \
           postgis=$POSTGIS_VERSION \
           python3 postgresql-plpython3-$PG_MAJOR \
           python3-requests python3-numpy \
           postgresql-$PG_MAJOR-pgrouting \
           postgresql-$PG_MAJOR-pgpointcloud \
           $BUILD_TOOLS
           
#      wget \
#      postgresql-$PG_MAJOR-pgrouting && 
#    rm -rf /var/lib/apt/lists/*

#Env fdw
ENV OWM_FWD_DEPS="libjson-c-dev libjson-c3 libprotobuf-c-dev protobuf-c-compiler libprotobuf-c1 zlib1g-dev zlib1g"

RUN apt-get install $OWM_FWD_DEPS -y --no-install-recommends
#OSM_fdw
RUN pgxn install osm_fdw

RUN apt-get purge -y --auto-remove $BUILD_TOOLS \
   && rm -rf /var/lib/apt/lists/*

#RUN mkdir -p /docker-entrypoint-initdb.d/
#COPY ./initdb-pgrouting.sh /docker-entrypoint-initdb.d/routing.sh
