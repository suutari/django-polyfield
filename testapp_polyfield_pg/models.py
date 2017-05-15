from django.contrib.postgres import fields as pgfields
from django.db import models

from django_polyfield.postgres import PolyJsonField, PolyJsonListField
from testapp_polyfield_basic.animals import Animal


class PostgresJsonObject(models.Model):
    obj = PolyJsonField(Animal)
    bare_json = pgfields.JSONField()


class PostgresJsonList(models.Model):
    objs = PolyJsonListField(Animal)
    bare_json = pgfields.JSONField()
