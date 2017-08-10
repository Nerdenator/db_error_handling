# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import connection, DatabaseError, transaction

from django.db import models


class TestTable(models.Model):
    value1 = models.IntegerField()
    value2 = models.IntegerField()
    same = models.CharField(max_length=3, null=True)


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


def set_no():
    """
    sets "same" column on rows with differing value1 and value2 columns to "no"
    :return:
    """
    pass

def broken_query():
    """
    a function meant to break. there is no column named 'different', so this should cause
    a DatabaseError to be thrown upon execution.
    :return:
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

def bulk_set():
    pass