# prepare data
```
osm2pgsql -c --slim --database "postgres" -U "postgres" -W -H "gdi-2.manserv.net" -P "1111" hamburg-latest.osm.pbf
```

```sql

alter table planet_osm_roads
add source int;
alter table planet_osm_roads
add target int;
alter table planet_osm_roads
add cost float;
--create graph
SELECT pgr_createTopology ('planet_osm_roads', 0.00001, 'way', 'osm_id', 'source', 'target');

update planet_osm_roads
set cost = st_length(way)
```
# routing and visualisation in qgis
```sql
SELECT *
        FROM pgr_dijkstra(
                'SELECT id, source, target, cost FROM planet_osm_roads',
                1, 6, false
        );
-- visu
select r.*, g.way from planet_osm_roads as g
inner join(
SELECT *
        FROM pgr_dijkstra(
                'SELECT id, source, target, cost FROM planet_osm_roads',
                17390, 3, false
        ) )as r
on g.id = r.edge;
```
# one to many (cost)
```sql
SELECT seq, id1 AS source, id2 AS target, cost
FROM pgr_kdijkstraCost(
                'SELECT id::int, source::int4, target::int4, cost::float8 FROM planet_osm_roads where cost >= 0',
                34, array [874,754], false, false
        );		
```
# one to many (path / spidergraph)
```sql
select distinct r.*, g.way from planet_osm_roads as g
inner join
(
SELECT seq, id1 AS path, id2 AS edge, cost
FROM pgr_kdijkstraPath(
                'SELECT id::int, source::int4, target::int4, cost::float8 FROM planet_osm_roads where cost >= 0',
                34, array [874,754], false, false
        )) as r
		on g.source = r.edge;
```

