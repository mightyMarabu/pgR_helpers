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
SELECT seq, id1 AS source, id2 AS target, cost FROM pgr_kdijkstraCost(
    'SELECT id, source, target, cost FROM edge_table',
    10, array[4,12], false, false
);
```
# one to many (path / spidergraph)
```sql

```

