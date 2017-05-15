import json

import pytest
from django.core import serializers
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from django_polyfield import Dictable, ObjectList
from testapp_polyfield_basic.animals import Bird, Worm
from testapp_polyfield_basic.models import FunnyContainer, Herd


class NonAnimal(Dictable):
    def __init__(self, key=''):
        self.key = key

    def __repr__(self):
        return 'NonAnimal({!r})'.format(self.key)

    def to_dict(self):
        return {'key': self.key}

    @classmethod
    def from_dict(cls, data):
        return cls(key=data['key'])


@pytest.mark.django_db
def test_polylistfield_roundtrip():
    herd = Herd()
    herd.animals.extend([Bird('Bob', 'm'), Worm('Wally')])
    herd.save()
    assert Herd.objects.get(pk=herd.pk).animals == herd.animals


@pytest.mark.django_db
def test_polyfield_roundtrip():
    herd = Herd()
    herd.leader = Bird('Eagle', 'f')
    herd.save()
    assert Herd.objects.get(pk=herd.pk).leader == herd.leader


@pytest.mark.django_db
def test_polyfield_invalid_subclass():
    herd = Herd()
    herd.leader = NonAnimal()  # TODO: How to raise TypeError here?
    with pytest.raises(TypeError):
        herd.save()


@pytest.mark.django_db
def test_polylistfield_invalid_subclass():
    herd = Herd()
    herd.animals.extend([Bird('Bob', 'm'), NonAnimal()])  # TODO: Raise here
    with pytest.raises(TypeError):
        herd.save()


@pytest.mark.django_db
def test_polylistfield_invalid_container():
    herd = Herd()
    herd.animals = Bird('Bob', 'm')  # TODO: Make this raise
    with pytest.raises(TypeError):
        herd.save()


@pytest.mark.django_db
def test_polyfield_default_value():
    herd = Herd()
    assert herd.leader is None
    herd.save()
    assert herd.leader is None
    assert Herd.objects.get(pk=herd.pk).leader is None


@pytest.mark.django_db
def test_polylistfield_default_value():
    herd = Herd()
    assert herd.animals == ObjectList()
    herd.save()
    assert herd.animals == ObjectList()
    assert Herd.objects.get(pk=herd.pk).animals == ObjectList()


def test_full_clean():
    herd = FunnyContainer(owner=Worm('X'), contents=ObjectList([Worm('A')]))
    herd.full_clean()  # Doesn't raise


def test_full_clean_detects_not_null():
    obj = FunnyContainer()
    with pytest.raises(ValidationError) as excinfo:
        obj.full_clean()
    assert str(excinfo.value) == "{'owner': ['This field cannot be null.']}"


@pytest.mark.django_db
def test_save_with_not_null():
    obj = FunnyContainer()  # No "owner", even though it's required
    with pytest.raises(IntegrityError):
        obj.save()


@pytest.mark.django_db
def test_polyfield_without_superclass():
    owner = NonAnimal('Owner')
    contents = ObjectList([NonAnimal('A'), Worm('Wax'), NonAnimal('B')])
    obj = FunnyContainer(owner=owner, contents=contents)
    obj.save()
    loaded = FunnyContainer.objects.get(pk=obj.pk)
    assert loaded.owner == owner
    assert loaded.contents == contents


@pytest.mark.django_db
def test_serialization_roundtrip():
    """
    Test serialized data can be deserialized correctly.
    """
    # Create object
    owner = NonAnimal('Owner')
    contents = ObjectList([NonAnimal('A'), Worm('Wax'), NonAnimal('B')])
    obj = FunnyContainer(owner=owner, contents=contents)
    obj.save()

    # Serialize
    objects = FunnyContainer.objects.filter(pk=obj.pk)
    json_string = serializers.serialize('json', objects)

    # Deserialize
    deserialized_objs = list(serializers.deserialize('json', json_string))
    deserialized_obj = deserialized_objs[0].object

    # Check object data
    assert deserialized_obj.owner == owner
    assert deserialized_obj.contents == contents
    assert deserialized_obj.parent is None
    assert isinstance(deserialized_obj.owner, NonAnimal)
    assert isinstance(deserialized_obj.contents[0], NonAnimal)


@pytest.mark.django_db
def test_polyfields_with_django_serializer():
    # Create object
    owner = NonAnimal('Owner')
    contents = [NonAnimal('B'), Bird('Donald', 'm'), NonAnimal('A')]
    obj = FunnyContainer(owner=owner, contents=ObjectList(contents))
    obj.save()

    # Serialize
    objects = FunnyContainer.objects.filter(pk=obj.pk)
    json_string = serializers.serialize('json', objects)

    # Check serialized data
    serialized_data = json.loads(json_string)
    nonanimal_type = __name__ + '.NonAnimal'
    bird_type = 'testapp_polyfield_basic.animals.Bird'
    assert serialized_data == [{
        'model': 'testapp_polyfield_basic.funnycontainer',
        'pk': obj.pk,
        'fields': {
            'contents': [
                {'type': nonanimal_type, 'data': {'key': 'B'}},
                {'type': bird_type, 'data': {'name': 'Donald', 'sex': 'm'}},
                {'type': nonanimal_type, 'data': {'key': 'A'}},
            ],
            'owner': {'type': nonanimal_type, 'data': {'key': 'Owner'}},
            'parent': None,
            'bird': {'type': bird_type, 'data': {'name': 'Daisy', 'sex': 'f'}},
        },
    }]
