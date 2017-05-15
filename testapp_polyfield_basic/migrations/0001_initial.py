# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import django_polyfield
import testapp_polyfield_basic.animals
from testapp_polyfield_basic.serializers import PickleSerializer


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FunnyContainer',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', django_polyfield.PolyField()),
                ('contents', django_polyfield.PolyListField()),
                ('parent',
                 django_polyfield.PolyField(blank=True, null=True)),
                ('bird',
                 django_polyfield.PolyField(
                     default=testapp_polyfield_basic.models.get_default_bird,
                     object_type=testapp_polyfield_basic.animals.Bird)),
            ],
        ),
        migrations.CreateModel(
            name='Herd',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True, serialize=False, verbose_name='ID')),
                ('leader', django_polyfield.PolyField(
                    blank=True, null=True,
                    object_type=testapp_polyfield_basic.animals.Animal)),
                ('animals', django_polyfield.PolyListField(
                    object_type=testapp_polyfield_basic.animals.Animal)),
            ],
        ),
        migrations.CreateModel(
            name='PickledHerd',
            fields=[
                ('id', models.AutoField(
                    auto_created=True,
                    primary_key=True, serialize=False, verbose_name='ID')),
                ('leader',
                 django_polyfield.PolyField(
                     blank=True, null=True,
                     object_type=testapp_polyfield_basic.animals.Animal,
                     serializer_class=PickleSerializer)),
                ('animals',
                 django_polyfield.PolyListField(
                     object_type=testapp_polyfield_basic.animals.Animal,
                     serializer_class=PickleSerializer)),
            ],
        ),
    ]
