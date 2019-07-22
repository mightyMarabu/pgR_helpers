## create function
```sql
create or replace function mafma.geomfromcoords(
x float,
y float) 

returns table (geom geometry)
language  'sql'
as

$BODY$
select st_setsrid(st_makepoint(x,y),4326)
$BODY$
```


# python & pgsql-loops

## python example
```sql
CREATE OR REPLACE FUNCTION pymax(
	a integer,
	b integer)
    RETURNS TABLE(x integer, y integer) 
    LANGUAGE 'plpython3u'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$

 import requests
 return [(a, b), (b, a)]# [{"x": a, "y": b}]

$BODY$;
```
## python api request
```sql

CREATE OR REPLACE FUNCTION routing.use_dts(
	x double precision,
	y double precision,
	maxval double precision DEFAULT 2)
    RETURNS TABLE(id integer, x double precision, y double precision, dt double precision, distance double precision) 
    LANGUAGE 'plpython3u'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$

 import requests
 
 API = "https://dts-int-dts-1.dmz.manserv.net/api/Reach"
 # API = "http://dev-geo-2/drivetimes/api/Reach"
 params = {
 	"lat": y,
    "lng": x,
    "maxVal": maxval,
    "direction": 1,
    "valuation": 1,
	"reachReturnType": 0
 }
 response = requests.get(API, params = params, verify = False)
 data = response.json()
 plpy.notice(response.url)
 plpy.notice("Count %i" % data["Count"])
 
 f = lambda x: 1 if x < 5 else 2 
 
 result = [(f(item[2]), item[1], item[0], item[2], item[3]) for item in data["Items"]]
 return result

$BODY$;
```
## multipont-dt

```sql
CREATE OR REPLACE FUNCTION mafma.use_dts_multipoints()
    RETURNS void
    LANGUAGE 'plpgsql'

AS $BODY$

DECLARE target RECORD;
BEGIN
   FOR target IN select r.id, r.dt, r.geom,x,y from mafma.rawdata as r LOOP -- set iteration limit
RAISE NOTICE '% done!', target.id;
      insert into mafma.dt_result(id_s, geom, id, x , y , dt , distance )
      SELECT target.id as id_s, ST_SetSRID(ST_MakePoint(x,y),4326), * from mafma.use_dts(
          target.x, target.y,target.dt 
          ); END LOOP;
   END;
$BODY$;
```

### anpassen der tabellen:

```sql
alter table mafma.rawdata
add dt int;
alter table mafma.dt_result
add id_s int;

update mafma.rawdata
set dt =  10;
```

## create trigger-function
```sql
CREATE OR REPLACE FUNCTION mafma.trigger_geomfromcoords()
    RETURNS trigger
    LANGUAGE 'plpgsql'
AS 
$BODY$
BEGIN
update mafma.rawdata
set geom = st_setsrid(st_makepoint(x,y),4326)
where x is not null and y is not null;
RETURN NULL;
END;
$BODY$;
```

## create trigger

```sql
CREATE TRIGGER update_geom
  AFTER INSERT
  ON mafma.rawdata
  FOR EACH ROW
  EXECUTE PROCEDURE mafma.trigger_geomfromcoords();
```
