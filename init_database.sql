-------------------------------------------------------------------------------
-- Database Initialization Script --
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
-- POSTGIS Spatial Model - Full support for Spatial/GIS columns, indexes
-------------------------------------------------------------------------------
-- CSV: region,origin_coord,destination_coord,datetime,datasource
-- https://learn.crunchydata.com/postgis/qpostgisintro/

-- DROP TABLE IF EXISTS trip_geom;

CREATE TABLE IF NOT EXISTS trip_geom
(
    region VARCHAR(255) NOT NULL,
    origin_coord geography(Point,4326) NOT NULL,
    destination_coord geography(Point,4326) NOT null,
    tripdate TIMESTAMP NOT NULL,
    datasource VARCHAR(255) NOT NULL
);

CREATE INDEX IF NOT EXISTS trip_geom_origin_coord_idx
  ON trip_geom USING GIST (origin_coord);

CREATE INDEX IF NOT EXISTS trip_geom_destination_coord_idx
  ON trip_geom USING GIST (destination_coord);

-------------------------------------------------------------------------------
-- OLAP Model - Basic or No support for Spatial/GIS, Some UDF support
-------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS trip_fact
(
    region VARCHAR(255) NOT NULL,
    datasource VARCHAR(255) NOT NULL,
    tripdate TIMESTAMP NOT NULL,
    lat1 float NOT NULL,
    lng1 float NOT NULL,
    lat2 float NOT NULL,
    lng2 float NOT NULL
);

CREATE TABLE IF NOT EXISTS region_dimension
(
    region VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS datasource_dimension
(
    datasource VARCHAR(255) NOT NULL
);

-------------------------------------------------------------------------------

-- select * from trip_fact limit 20
-- select * from region_dimension  limit 20

-------------------------------------------------------------------------------
-- End of Script --
-------------------------------------------------------------------------------
