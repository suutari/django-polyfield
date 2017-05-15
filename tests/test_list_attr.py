from django_polyfield._fields import PolyListAttribute
from testapp_polyfield_basic.models import Herd


def test_get_from_class():
    assert isinstance(Herd.animals, PolyListAttribute)
