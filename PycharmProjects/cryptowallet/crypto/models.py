# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=1000000)
    address = models.CharField(max_length=500)

    # Override String Representation
    def __str__(self):
        return self.name


class Transaction(models.Model):
    from_address = models.CharField(max_length=250)
    to_address = models.CharField(max_length=250)
    amount = models.CharField(max_length=250)

    def __str__(self):
        return self.from_address