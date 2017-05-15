from django.contrib.postgres import fields as pgfields

from . import _postgres_lookups as lookups
from ._fields import _ListSerialized, _SingleSerialized
from .serialization import DataSerializer


class PolyJsonField(_SingleSerialized, pgfields.JSONField):
    default_serializer_class = DataSerializer


class PolyJsonListField(_ListSerialized, pgfields.JSONField):
    default_serializer_class = DataSerializer


for cls in [PolyJsonField, PolyJsonListField]:
    cls.register_lookup(lookups.Exact)
    cls.register_lookup(lookups.DataContains)
    cls.register_lookup(lookups.ContainedBy)
