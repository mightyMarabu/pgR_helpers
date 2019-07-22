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
