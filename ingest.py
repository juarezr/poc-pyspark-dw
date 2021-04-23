#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""POC Ingestion Routine."""

import os
import sys
import shutil

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
        print("# Starting POC Ingestion Routine:")

        result = _run_tasks()

        print("# Finished Ingestion: %s" % result)

    except Exception as ex:  # pylint: disable=broad-except
        print("# FAILURE: {0}".format(ex))
        sys.exit(2)


if __name__ == "__main__":
    _run_program()

# endregion

# end of file #
