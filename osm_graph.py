# prepare data

import argparse
from os import getenv
import psycopg2
import time

ts_start = time.time()

#parser = argparse.ArgumentParser()
#parser.add_argument("-H", "--host", help="host location of postgres database", type=str)
#parser.add_argument("-U", "--user", help="username to connect to the database", type=str)
#parser.add_argument("-d", "--dbname", help="database name", type=str)
#parser.add_argument("-p", "--port", help="port to connect to postgres", type=str)
#args = parser.parse_args()
#password = "postgres" #getenv('PW')

#print(args)

conn = psycopg2.connect(
    #f"dbname={args.dbname} user={args.user} host={args.host} port={args.port} password={password}"
    "dbname=OSM user=postgres host=gdi-1.manserv.net port=7777 password=postgres"

)
cur = conn.cursor()
print("connected to database")

print("preparing data")

cur.execute("DROP TABLE IF EXISTS routing.route;\
            create table routing.route as\
            SELECT *, ST_Transform(ST_SetSRID(way,900913),3112) as geom \
            FROM planet_osm_roads where highway is not null and highway not in ('path', 'track');\
            ALTER TABLE routing.route ADD id serial;\
            ALTER TABLE routing.route DROP COLUMN way;")
print("route table created")

cur.execute("DROP TABLE IF EXISTS routing.testrouteexplode;\
            create table routing.testrouteexplode as\
            WITH segments AS (\
            SELECT id, ST_MakeLine(lag((pt).geom, 1, NULL) OVER (PARTITION BY id ORDER BY id, (pt).path), (pt).geom) AS geom\
            FROM (SELECT id, ST_DumpPoints(geom) AS pt FROM routing.route) as dumps)\
            SELECT * FROM segments WHERE geom IS NOT NULL;")
#            SELECT UpdateGeometrySRID('routing','testrouteexplode','geom',900913);")

print("explode table created")

cur.execute("alter table routing.testrouteexplode add old_id int;\
                update routing.testrouteexplode set old_id = id;\
            alter table routing.testrouteexplode drop column id;\
            alter table routing.testrouteexplode add id serial;")
cur.execute("DROP TABLE IF EXISTS routing.preparedforrouting;\
            create table routing.preparedforrouting as \
            select old_id::int as id,(st_dump(st_linemerge(st_union(geom)))).geom from routing.testrouteexplode group by old_id;")
#            SELECT UpdateGeometrySRID('routing','preparedforrouting','geom',900913);")
print("routing table created")

cur.execute("alter table routing.preparedforrouting add source int;\
            alter table routing.preparedforrouting add target int;\
            alter table routing.preparedforrouting add cost float;")
print("columns added")

cur.execute("update routing.preparedforrouting\
            set cost = st_length(geom);")
print("cost updated")


# create graph

cur.execute("SELECT MIN(id), MAX(id) FROM routing.preparedforrouting;")

min_id, max_id = cur.fetchone()
print("creating graph: there are %s - %s edges to be processed" % (max_id, min_id + 1))
cur.close()

interval = 50000
for x in range(min_id, max_id+1, interval):
    cur = conn.cursor()
    cur.execute(
    "select pgr_createTopology('routing.preparedforrouting', 0.00001, 'geom', 'id', rows_where:='id>=%s and id<%s');" % (x, x + interval)
    )
    conn.commit()
    x_max = x + interval - 1
    if x_max > max_id:
        x_max = max_id
    print("edges %s - %s have be processed" % (x, x_max))

cur = conn.cursor()
cur.execute("""ALTER TABLE routing.preparedforrouting_vertices_pgr
  ADD COLUMN IF NOT EXISTS lat float8,
  ADD COLUMN IF NOT EXISTS lon float8;""")

cur.execute("""UPDATE routing.preparedforrouting_vertices_pgr
  SET lat = ST_Y(the_geom),
      lon = ST_X(the_geom);""")

conn.commit()
