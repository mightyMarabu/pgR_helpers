# foreign data wrapper
## osm_fdw
```sql
create server osm_fdw_server foreign data wrapper osm_fdw;

select create_osm_table('osm_hamburg', 'osm_fdw_server', '/data/hamburg-latest.osm.pbf');

select * from osm_hamburg LIMIT 10

select id, tags->>'name' as name, tags->>'operator' as operator,tags->>'website' as website, tags  
from osm_hamburg 
where tags->>'amenity'='fuel'
```
## postgres-fdw

```sql
-- Extension erzeugen/anlegen/aktivieren
create extension postgres_fdw;

-- foreign Server anlegen
create extension postgres_fdw;
--create foreign server
create server gdi1_osm
foreign data wrapper postgres_fdw
options (host 'gdi-1.manserv.net', dbname 'OSM', port '7777');
--user mapping
create user mapping for user server gdi1_osm--username
options (user 'postgres', password 'postgres');

--optinal: create schema
--import schema
IMPORT FOREIGN SCHEMA public
    LIMIT TO (planet_osm_point,planet_osm_polygon)
    FROM SERVER gdi1_osm
    INTO mafma;
```
