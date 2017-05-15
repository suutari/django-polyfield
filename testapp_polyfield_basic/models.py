from django.db import models

from django_polyfield import PolyField, PolyListField

from .animals import Animal, Bird
from .serializers import PickleSerializer


def get_default_bird():
    return Bird('Daisy', 'f')


class Herd(models.Model):
    leader = PolyField(Animal, null=True, blank=True)
    animals = PolyListField(Animal)


class FunnyContainer(models.Model):
    owner = PolyField()
    contents = PolyListField()
    parent = PolyField(null=True, blank=True)
    bird = PolyField(Bird, default=get_default_bird)


class PickledHerd(models.Model):
    leader = PolyField(Animal, serializer_class=PickleSerializer,
                       null=True, blank=True)
    animals = PolyListField(Animal, serializer_class=PickleSerializer)
