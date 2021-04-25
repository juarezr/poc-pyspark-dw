#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""POC Reporting Routine."""

import os
import sys
import shutil

# region Report

def report(spark):
    qr = spark.read.jdbc(url = "jdbc:postgresql://poc-dw:5432/poc",
            table = "(SELECT region,datasource,tripdate,lat1,lng1,lat2,lng2 from public.trip_fact) AS my_query",
            properties={"user": "poc", "password": "poc"}).createTempView('tbl')
    # without createTempView('tbl'), this command will return a DataFrame
    spark.sql('select * from tbl').show() #or use .collect() to get Rows

# endregion

# region Program Logic


def _do_something():
    return  'Hello World!'


def _run_tasks():
    print("# Doing somethin:")

    result = _do_something()

    return result

# endregion

# region Start of the program


def _run_program():
    try:
        print("# Starting POC Reporting Routine:")

        result = _run_tasks()

        print("# Finished Reporting: %s" % result)

    except Exception as ex:  # pylint: disable=broad-except
        print("# FAILURE: {0}".format(ex))
        sys.exit(2)


if __name__ == "__main__":
    _run_program()

# endregion

# end of file #
