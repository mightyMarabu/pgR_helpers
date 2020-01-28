FROM postgres:10

LABEL maintainer="Sebastian <sebastian.n.schmidt@gmail.com>"

# pgRouting
ENV PGROUTING_MAJOR 2.5
ENV PGROUTING_VERSION 2.5.2

# Postgis
ENV POSTGIS_MAJOR 2.5
ENV POSTGIS_VERSION 2.5.1+dfsg-1.pgdg90+1

# ENV PLPYTHON_VERSION 10.6-1.pgdg18.04+1

ENV BUILD_TOOLS="cmake make gcc libtool git python-setuptools postgresql-server-dev-$PG_MAJOR"

RUN apt-get update \
   && apt-get install -y --no-install-recommends \
      postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR=$POSTGIS_VERSION \
      postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR-scripts=$POSTGIS_VERSION \
      postgis=$POSTGIS_VERSION \
      python3 postgresql-plpython3-$PG_MAJOR \
      python3-requests \
      postgresql-$PG_MAJOR-pgrouting \
      $BUILD_TOOLS

# Install H3
RUN easy_install pgxnclient \
   && /usr/local/bin/pgxn install h3

# Clean up
RUN apt-get purge -y --auto-remove $BUILD_TOOLS \
   && rm -rf /var/lib/apt/lists/*
