# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class Module(models.Model):
    name = models.CharField(max_length=400, default="")
    attr_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Attribute(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default="")
    data_repo = models.CharField(max_length=200, default="")
    java_class = models.CharField(max_length=400, default="")
    num_dependencies = models.IntegerField(default=0)
    num_dependents = models.IntegerField(default=0)
    cti = ArrayField(ArrayField(models.CharField(max_length=200)))

    def __str__(self):
        return self.name
