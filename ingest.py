#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""POC Ingestion Routine."""

import os
import sys
import shutil

from pyspark.sql import SparkSession
from pyfiglet import figlet_format
from termcolor import cprint

# region Parameters

DB_URI = 'jdbc:postgresql://poc-dw:5432/poc?stringtype=unspecified'
DB_USR = 'poc'
DB_PWD = 'poc'

# endregion

# region Program Logic


def _read_trips(session, source_path, csv_schema=None):
    if csv_schema:
        reader = session.read.format("csv").schema(csv_schema)
    else:
        reader = session.read.format("csv")
    df = reader.option("header", "true").load(source_path)
    return df


def _rename_cols(csv):
    res = csv.withColumnRenamed('datetime', 'tripdate')
    return res


def _expand_coord(coord):
    nums = coord[7:-1]
    pair = nums.split(' ')
    res = (float(pair[1]), float(pair[0]))
    return res


def _expand_columns(row):
    lat1, lng1 = _expand_coord(row.origin_coord)
    lat2, lng2 = _expand_coord(row.destination_coord)
    vals = (row.region, row.datasource, row.datetime, lat1, lng1, lat2, lng2)
    return vals


def _expand_trips(csv):
    parsed = csv.rdd.map(_expand_columns)
    trips = parsed.toDF(['region', 'datasource', 'tripdate', 'lat1', 'lng1', 'lat2', 'lng2'])
    return trips.alias('trip')


def _ingest_into_db(df, table_name):
    _print_df(df, table_name)
    # Spark batch write into postgresql
    df.write.format("jdbc") \
        .option("url", DB_URI) \
        .option("user", DB_USR).option("password", DB_PWD) \
        .option("dbtable", table_name) \
        .mode("append") \
        .save()


def _inform_user():
    message = figlet_format("Success:\nTrips Imported")
    cprint(message, 'yellow', 'on_red', attrs=['bold'])


# endregion

# region Spark helpers

def _init_session():
    session = SparkSession.builder \
        .master("local[*]") \
        .appName("poc-etl") \
        .getOrCreate()
    return session


def _print_df(df, title=None, rows=4):
    if title:
        print("# Dataframe %s - Schema/Samples" % title)
    df.printSchema()
    df.show(rows, False)


# endregion

# region Start of the program


def _run_tasks():
    print("# Starting Spark standalone session...")
    session = _init_session()

    print("# Reading trips from CSV file...")
    csv = _read_trips(session, '/root/trips.csv')

    print("# Transforming spatial columns...")
    trips = _expand_trips(csv)

    print("# Ingesting into OLAP database...")
    _ingest_into_db(trips, "public.trip_fact")

    print("# Ingesting into Spatial database...")
    ins = _rename_cols(csv)
    _ingest_into_db(ins, "public.trip_geom")

    # TODO: run a query with WINDOW FUNCTIONS for locating and deduping similar trips

    _inform_user()


def _run_program():
    print("# Starting POC Ingestion Routine...")
    try:
        _run_tasks()
    except Exception as ex:  # pylint: disable=broad-except
        print("# FAILURE: {0}".format(ex))
        sys.exit(2)

    print("# Finished POC Ingestion Routine.")


if __name__ == "__main__":
    _run_program()

# endregion

# end of file #
