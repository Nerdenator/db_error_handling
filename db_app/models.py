# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import connection, DatabaseError, transaction
import pandas as pd

from django.db import models


class TestTable(models.Model):
    value1 = models.IntegerField()
    value2 = models.IntegerField()
    same = models.CharField(max_length=3, null=True)


def setup_table():
    """
    sets up the basic table.
    several rows will have matching values, some won't.
    :return: None
    """
    row1 = TestTable(value1=1, value2=1)
    row1.save()

    row2 = TestTable(value1=2, value2=1)
    row2.save()

    row3 = TestTable(value1=56, value2=1)
    row3.save()

    row4 = TestTable(value1=10, value2=10)
    row4.save()


def set_yes():
    """
    sets "same" column on rows with matching value1 and value2 columns to "yes"
    :return: None
    """
    query = '''
        UPDATE db_app_testtable
        SET same = 'yes'
        WHERE value1 = value2
    '''
    try:
        with transaction.atomic():
            cursor = connection.cursor()
            cursor.execute(query)
    except DatabaseError as ex:
        print "set_yes has error %s" % (ex)
        raise
    finally:
        cursor.close()
        print_table()


def set_no():
    """
    sets "same" column on rows with differing value1 and value2 columns to "no"
    :return: None
    """
    query = '''
        UPDATE db_app_testtable
        SET same = 'no'
        WHERE value1 != value2
    '''
    try:
        with transaction.atomic():
            cursor = connection.cursor()
            cursor.execute(query)
    except DatabaseError as ex:
        print "set_no has error %s" % (ex)
        raise
    finally:
        cursor.close()
        print_table()


def broken_query():
    """
    a function meant to break. there is no column named 'different', so this should cause
    a DatabaseError to be thrown upon execution.
    :return: None
    """
    query = '''
        UPDATE db_app_testtable
        SET different = 'lol no'
        WHERE value1 = value2
    '''
    try:
        with transaction.atomic():
            cursor = connection.cursor()
            cursor.execute(query)
    except DatabaseError as ex:
        print "broken_query has error %s" % (ex)
        raise
    finally:
        cursor.close()


def print_table():
    query = '''
        SELECT * FROM db_app_testtable;
    '''

    # No transaction needed for SELECT operations.
    # using a pandas dataframe per:
    # https://stackoverflow.com/questions/37051516/printing-a-properly-formatted-sqlite-table-in-python
    print pd.read_sql_query(query, connection)


def reset_table():
    """
    puts all "same" column back to null
    :return:
    """
    query = '''
        UPDATE db_app_testtable
        SET same = NULL 
        WHERE same = "yes" OR same ="no"
    '''
    try:
        with transaction.atomic():
            cursor = connection.cursor()
            cursor.execute(query)
    except DatabaseError as ex:
        print "reset_table has error % s" % (ex)
        raise
    finally:
        cursor.close()
        print_table()


def bulk_set():
    try:
        set_no()
        set_yes()
        broken_query()
    except Exception as gen_ex:
        print "Exception has occurred."
        raise
