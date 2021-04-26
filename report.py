#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""POC Reporting Routine."""

import os
import sys
import shutil

from pyspark.sql import SparkSession

# region Parameters

DB_URI = 'jdbc:postgresql://poc-dw:5432/poc'
DB_USR = 'poc'
DB_PWD = 'poc'

# -------|-------------------------------------------------------------------------------
# region |bounding box
# -------|-------------------------------------------------------------------------------
# Hamburg|LINESTRING(9.80304883152659 53.4286593358781,10.2154964127794 53.6522012107166)
# Prague |LINESTRING(14.3184039058018 49.9898055746658,14.6668925739693 50.1250223347743)
# Turin  |LINESTRING(7.51313508795287 44.9761246656205,7.73966001978033 45.1393010284832)

FILTER_BBOX = 'LINESTRING(7.51313508795287 44.9761246656205,7.73966001978033 45.1393010284832)'

FILTER_REGION = 'Turin'

FILTER_DATE_INI = '2018-05-13'
FILTER_DATE_FIN = '2018-05-23'

# endregion

# region Program Logic

REPORT_AVG = '''
    WITH trips_cte AS (
        SELECT tripdate
        FROM trip_geom
        WHERE tripdate IS NOT null
        AND region = '%s'
        AND tripdate BETWEEN '%s 00:00:00' AND '%s 00:00:00'
        AND ST_Intersects(ST_MakeLine(origin_coord::geometry, destination_coord::geometry),
            ST_Envelope(ST_GeomFromText('SRID=4326;%s')))
    )
    SELECT 'Week' as Metric
        , date_trunc('week', tripdate)::date || ' - ' || (date_trunc('week', tripdate) + '6 days') ::date AS Weeks
        , count(*) as Trips
    FROM trips_cte
    GROUP BY 2
    UNION ALL
    SELECT 'Average' as Metric
        , min(tripdate)::date || ' - ' || max(tripdate)::date AS Weeks
        , count(*) / nullif(count(distinct extract(week from tripdate)),0) AS Trips
    FROM trips_cte
'''

# endregion

# region Spark helpers

def _init_session():
    session = SparkSession.builder \
        .master("local[*]") \
        .appName("poc-etl") \
        .getOrCreate()
    return session


def _run_spark_report(session, sql, *args):
    query = _fill_params(sql, *args)
    res = _query_db(session, query)
    _print_df(res)
    return res


def _query_db(session, sql):
    query_sql = "(%s) AS my_query" % sql
    df = session.read.jdbc(url = DB_URI,
            table = query_sql,
            properties={"user": DB_USR, "password": DB_PWD})
    return df


def _fill_params(sql, *args):
    pars = tuple(args)
    resq = sql % pars
    return resq


def _print_df(df, title=None, rows=100):
    if title:
        print("# %s #" % title)
    df.show(rows, False)


# endregion

# region Start of the program


def _run_tasks():
    print("# Starting Spark standalone session...")
    session = _init_session()

    msg = "\n# Building Trips Average Report with:\n# Region: %s\n# Date  : %s -> %s\n# Box   : %s\n"
    print(msg % (FILTER_REGION, FILTER_DATE_INI, FILTER_DATE_FIN, FILTER_BBOX))

    _run_spark_report(session, REPORT_AVG, FILTER_REGION, FILTER_DATE_INI, FILTER_DATE_FIN, FILTER_BBOX)


def _run_program():
    print("# Running POC Reports Routine...")
    try:
        _run_tasks()
    except Exception as ex:  # pylint: disable=broad-except
        print("# FAILURE: {0}".format(ex))
        sys.exit(2)

    print("# Finished POC Reports Routine.")


if __name__ == "__main__":
    _run_program()

# endregion

# end of file #
