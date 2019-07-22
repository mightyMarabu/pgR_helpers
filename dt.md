## Fahrzeit

```sql
select * from mafma.use_dts(10,53.5,5)
```

```sql
truncate table mafma.dt_result;
insert into mafma.dt_result
select *, st_setsrid(st_makepoint(x,y),4326) as geom 
from mafma.use_dts(10,53.5,5)
```

## Welche Gebiete werden erreicht?

```sql
select distinct b.name, b.way, avg(r.dt)
from mafma.dt_result as r, mafma.ger_admin_bounds_10 as b
where st_contains(b.way,(st_transform(r.geom,900913))) = true
group by b.name, b.way
```

## alles zusammen..

```sql
select distinct b.name, b.way, avg(r.dt)
from mafma.use_dts(
            (select x from mafma.rawdata where id = 6),
            (select y from mafma.rawdata where id = 6),
             15
                    ) as r, 
mafma.ger_admin_bounds_10 as b
where   st_contains(b.way,(st_transform((st_setsrid(st_makepoint(r.x,r.y),4326)),900913))) = true
group by b.name, b.way
```

# pgRouting
### alphashape

```sql
select * from mafma.use_pgr_area(
    (select x from mafma.rawdata where id = 7),
    (select y from mafma.rawdata where id = 7),
    50)
```
### tsp
```sql
truncate mafma.tsp_result;
insert into mafma.tsp_result
with tsp as 
(
select tsp.*, g.geom
from pgr_tsp('select id, x, y from mafma.rawdata', 14, 11) as tsp
inner join mafma.rawdata as g on tsp.id1 = g.id
)
select st_transform(st_makeline(geom order by seq), 900913) as line, sum(cost) as total_cost
from tsp
```

# graphhopper

```sql
select * from pgr_pointsaspolygon(
    'SELECT id, lng as x, lat as y from
    routing.use_graphhopper(-37.716418,145.038757,600)',0.0001);
```
