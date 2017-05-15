# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models

import django_polyfield.postgres
import testapp_polyfield_basic.animals


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PostgresJsonList',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True, serialize=False, verbose_name='ID')),
                ('objs', django_polyfield.postgres.PolyJsonListField(
                    object_type=testapp_polyfield_basic.animals.Animal)),
                ('bare_json',
                 django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='PostgresJsonObject',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True, serialize=False, verbose_name='ID')),
                ('obj', django_polyfield.postgres.PolyJsonField(
                    object_type=testapp_polyfield_basic.animals.Animal)),
                ('bare_json',
                 django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
    ]
