from django.contrib.postgres import fields as pgfields
from django.contrib.postgres import lookups as pglookups
from django.db.models import lookups as builtin_lookups


class PolyJsonFieldLookup(object):
    def get_prep_lookup(self):
        field = self.lhs.output_field
        return pgfields.JSONField.get_prep_value(field, self.rhs)


class Exact(PolyJsonFieldLookup, builtin_lookups.Exact):
    pass


class DataContains(PolyJsonFieldLookup, pglookups.DataContains):
    pass


class ContainedBy(PolyJsonFieldLookup, pglookups.ContainedBy):
    pass
