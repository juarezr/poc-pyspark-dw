#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""POC Ingestion Routine."""

import os
import sys
import shutil

from pyspark.sql import SparkSession

# region Program Logic

def _init_session():
    session = SparkSession.builder \
        .master("local[*]") \
        .appName("poc-spark-etl") \
        .getOrCreate()
    return session


def _read_trips(session, source_path, csv_schema=None):
    if csv_schema:
        reader = session.read.format("csv").schema(csv_schema)
    else:
        reader = session.read.format("csv")
    df = reader.option("header", "true").load(source_path)
    return df


def _expand_coord(coord):
    nums = coord[7:-1]
    pair = nums.split(' ')
    res = (float(pair[0]), float(pair[1]))
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


def _ingest_into_dw(trips):
    trips.write.format("jdbc") \
        .option("url", "jdbc:postgresql://poc-dw:5432/poc") \
        .option("dbtable", "public.trip_fact") \
        .option("user", "poc").option("password", "poc") \
        .mode("overwrite").save()


# endregion

# region Start of the program


def _run_tasks():
    print("# Starting Spark standalone session...")
    session = _init_session()

    print("# Reading trips from CSV file...")
    csv = _read_trips(session, '/root/trips.csv')

    print("# Transforming columns...")
    trips = _expand_trips(csv)

    trips.printSchema()
    trips.show()

    print("# Ingesting into database...")
    _ingest_into_dw(trips)


def _run_program():
    print("# Starting POC Ingestion Routine...")
    try:
        _run_tasks()
    except Exception as ex:  # pylint: disable=broad-except
        print("# FAILURE: {0}".format(ex))
        sys.exit(2)

    print("# Finished POC Ingestion Routine.")


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
