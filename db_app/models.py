# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import connection, DatabaseError

from django.db import models

class TestTable(models.Model):
    value1 = models.IntegerField()
    value2 = models.IntegerField()
    same = models.CharField(max_length=3)


def set_yes():
    pass

def set_no():
    pass