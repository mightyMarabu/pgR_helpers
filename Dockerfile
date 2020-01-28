FROM postgres:11
MAINTAINER Sebastian <sebastian.n.schmidt@gmail.com>

ENV POSTGIS_MAJOR 2.5
ENV POSTGIS_VERSION 2.5.2+dfsg-1~exp1.pgdg90+1
ENV PGROUTING_MAJOR 2.5
ENV PGROUTING_VERSION 2.5.2

RUN apt-get update \
      && apt-cache showpkg postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR \
      && apt-get install -y --no-install-recommends \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR=$POSTGIS_VERSION \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR-scripts=$POSTGIS_VERSION \
           postgis=$POSTGIS_VERSION 
#      && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /docker-entrypoint-initdb.d

ENV BUILD_TOOLS="cmake make gcc libtool git pgxnclient postgresql-server-dev-$PG_MAJOR"

#ENV PLPYTHON_VERSION 10.6-1.pgdg18.04+1
# python extension
RUN apt-get install -y --no-install-recommends \
           python3 postgresql-plpython3-$PG_MAJOR \
           python3-requests python3-numpy \
           postgresql-$PG_MAJOR-pgrouting \

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

RUN mkdir -p /docker-entrypoint-initdb.d/
#COPY ./initdb-pgrouting.sh /docker-entrypoint-initdb.d/routing.sh
