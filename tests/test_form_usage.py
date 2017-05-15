import pytest
from django.forms import CharField, Textarea

from django_polyfield import PolyField, PolyListField

try:
    from django.contrib.postgres import forms as pgforms
    from django_polyfield.postgres import PolyJsonField, PolyJsonListField
except ImportError:
    pgforms = None
    PolyJsonField = 'PolyJsonField'
    PolyJsonListField = 'PolyJsonListField'


@pytest.mark.parametrize('field', [PolyField, PolyListField])
def test_formfield(field):
    formfield = field().formfield()
    assert isinstance(formfield, CharField)
    assert isinstance(formfield.widget, Textarea)


@pytest.mark.parametrize('field', [PolyJsonField, PolyJsonListField])
def test_pg_formfield(field):
    if isinstance(field, str):
        pytest.skip('No PostgreSQL fields available')

    formfield = field().formfield()
    assert isinstance(formfield, pgforms.JSONField)
    assert isinstance(formfield.widget, Textarea)
