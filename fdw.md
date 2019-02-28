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
