import pytest

from django_polyfield import ObjectList
from testapp_polyfield_basic.animals import Bird, Worm
from testapp_polyfield_basic.models import Herd


@pytest.mark.django_db
def test_normal_list_in_polylist_init():
    herd = Herd(animals=[Worm('X'), Worm('B')])
    assert isinstance(herd.animals, ObjectList)
    herd.save()


@pytest.mark.django_db
def test_normal_list_in_polylist_assign():
    herd = Herd()
    assert isinstance(herd.animals, ObjectList)
    herd.animals = [Worm('X'), Worm('B')]
    assert isinstance(herd.animals, ObjectList)
    herd.save()


@pytest.mark.django_db
def test_normal_list_in_polylist_assign_again():
    herd = Herd()
    assert isinstance(herd.animals, ObjectList)
    herd.animals = [Worm('X'), Worm('B')]
    assert isinstance(herd.animals, ObjectList)
    herd.animals = [Worm('Y'), Worm('A')]
    assert isinstance(herd.animals, ObjectList)
    herd.save()


@pytest.mark.django_db
def test_normal_list_in_polylist_create():
    herd = Herd.objects.create(animals=[Worm('X'), Worm('B')])
    assert isinstance(herd.animals, ObjectList)


def test_list_operations():
    herd = Herd(animals=[Bird('A', 'f'), Worm('X'), Bird('B', 'm'), Worm('Y')])
    assert isinstance(herd.animals, ObjectList)
    assert len(herd.animals) == 4
    assert herd.animals[0] == Bird('A', 'f')
    assert herd.animals[-1] == Worm('Y')
    assert list(herd.animals.instances_of(Worm)) == [Worm('X'), Worm('Y')]
