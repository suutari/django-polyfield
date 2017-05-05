Django Polyfield
================

Django Polyfield makes it possible to have a field in a Django model
with polymorphic class.  The field could have a single instance or a
list of instances which could have different classes.  Only requirement
is that all of the classes are derived from PolyObject and implement
JSON serialization.
