# prepare data

import argparse
from os import getenv
import psycopg2

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

cur.execute("DROP TABLE IF EXISTS routing.testrouteexplode;\
            create table routing.testrouteexplode as\
            WITH segments AS (\
            SELECT id, ST_MakeLine(lag((pt).geom, 1, NULL) OVER (PARTITION BY id ORDER BY id, (pt).path), (pt).geom) AS geom\
            FROM (SELECT id, ST_DumpPoints(geom) AS pt FROM routing.testroute) as dumps)\
            SELECT * FROM segments WHERE geom IS NOT NULL;")
print("explode table created")

cur.execute("alter table routing.testrouteexplode add old_id int;\
            alter table routing.testrouteexplode drop column id;\
            alter table routing.testrouteexplode add id serial;")
cur.execute("DROP TABLE IF EXISTS routing.preparedforrouting;\
            create table routing.preparedforrouting as \
            select old_id,(st_dump(st_linemerge(st_union(geom)))).geom from routing.testrouteexplode group by old_id;")
print("routing table created")


#alter table routing.testrouteexplode add source int;
#alter table routing.testrouteexplode add target int;
#alter table routing.testrouteexplode add cost float;

#update routing.testrouteexplode
#set cost = st_length(geom);")

##################################################################################
"""
#cur.execute("SELECT MIN(id), MAX(id) FROM routing.roads;")
#cur.execute("SELECT MIN(id), MAX(id) FROM routing.belgiumroads;")
cur.execute("SELECT MIN(id), MAX(id) FROM routing.australianroads;")


min_id, max_id = cur.fetchone()
print("there are %s - %s edges to be processed" % (max_id, min_id + 1))
cur.close()

interval = 50000
for x in range(min_id, max_id+1, interval):
    cur = conn.cursor()
    cur.execute(
#    "select pgr_createTopology('routing.roads', 0.001, 'way', 'osm_id', rows_where:='osm_id>=%s and osm_id<%s');" % (x, x + interval)
#    "select pgr_createTopology('routing.roads', 0.00001, 'way', 'id', rows_where:='id>=%s and id<%s');" % (x, x + interval)
#    "select pgr_createTopology('routing.belgiumroads', 0.00001, 'geom', 'id', rows_where:='id>=%s and id<%s');" % (x, x + interval)
    "select pgr_createTopology('routing.australianroads', 0.00001, 'geom', 'id', rows_where:='id>=%s and id<%s');" % (x, x + interval)

)
    conn.commit()
    x_max = x + interval - 1
    if x_max > max_id:
        x_max = max_id
    print("edges %s - %s have be processed" % (x, x_max))

cur = conn.cursor()
cur.execute("""ALTER TABLE routing.australianroads_vertices_pgr
  ADD COLUMN IF NOT EXISTS lat float8,
  ADD COLUMN IF NOT EXISTS lon float8;""")

cur.execute("""UPDATE routing.australianroads_vertices_pgr
  SET lat = ST_Y(the_geom),
      lon = ST_X(the_geom);""")
"""
conn.commit()
