import json

import pytest
from django.core import serializers

from django_polyfield import ObjectList
from testapp_polyfield_basic.animals import Bird, Worm
from testapp_polyfield_basic.models import PickledHerd


@pytest.mark.django_db
def test_pickled_polylistfield_roundtrip():
    herd = PickledHerd()
    herd.animals = ObjectList([Bird('Bob', 'm'), Worm('Wally')])
    herd.save()
    assert PickledHerd.objects.get(pk=herd.pk).animals == herd.animals


@pytest.mark.django_db
def test_pickled_polyfield_roundtrip():
    herd = PickledHerd()
    herd.leader = Bird('Eagle', 'f')
    herd.save()
    assert PickledHerd.objects.get(pk=herd.pk).leader == herd.leader


@pytest.mark.django_db
def test_pickled_with_django_serializer():
    """
    Test serializing Django object with pickled field to a stream.

    Note: When serializing objects with Django serialization interface
    (django.core.serializers), the dump method of the serializer_class
    is not called, but serialize method is.  This means that data is
    serialized in the dictionary format, but it is not pickled.
    """
    # Create object
    leader = Bird('Boss', 'f')
    animals = ObjectList([Worm('Joe'), Bird('Andy', 'm')])
    obj = PickledHerd(leader=leader, animals=animals)
    obj.save()

    # Serialize
    objects = PickledHerd.objects.filter(pk=obj.pk)
    json_string = serializers.serialize('json', objects)

    # Check serialized data
    serialized_data = json.loads(json_string)
    assert serialized_data == [{
        'model': 'testapp_polyfield_basic.pickledherd',
        'pk': obj.pk,
        'fields': {
            'animals': [
                {'D': {'name': 'Joe', 'age': 0},
                 'T': 'testapp_polyfield_basic.animals.Worm'},
                {'D': {'name': 'Andy', 'sex': 'm'},
                 'T': 'testapp_polyfield_basic.animals.Bird'}],
            'leader': {'D': {'name': 'Boss', 'sex': 'f'},
                       'T': 'testapp_polyfield_basic.animals.Bird'},
        },
    }]
