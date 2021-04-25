-- Database Initialization Script --

-- Source Columns: region,origin_coord,destination_coord,datetime,datasource

CREATE TABLE IF NOT EXISTS region_dimension
(
    region VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS datasource_dimension
(
    datasource VARCHAR(255) NOT NULL
);

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

-- select * from trip_fact
-- select * from region_dimension

-- End of Script --
