from django import forms
from django.db import models
from django.db.models.query_utils import DeferredAttribute
from django.utils.translation import ugettext_lazy as _

from ._dictable import Dictable
from ._list import ObjectList
from .serialization import JsonSerializer, Serializer


class _Serialized(object):
    def __init__(self, object_type=Dictable, serializer_class=None,
                 *args, **kwargs):
        """
        Construct the field.
        """
        assert issubclass(object_type, Dictable)
        kwargs.setdefault('default', self._poly_default)
        self.object_type = object_type
        self.serializer_class = (serializer_class or
                                 self.default_serializer_class)
        self.serializer = self.serializer_class(object_type)
        assert isinstance(self.serializer, Serializer)
        super(_Serialized, self).__init__(*args, **kwargs)

    def deconstruct(self):
        """
        Deconstruct this field.

        Django uses this method e.g. when creating migrations.
        """
        (name, path, args, kwargs) = super(_Serialized, self).deconstruct()
        if kwargs.get('default', 0) is self._poly_default:
            del kwargs['default']
        if self.object_type != Dictable:
            kwargs['object_type'] = self.object_type
        if self.serializer_class != self.default_serializer_class:
            kwargs['serializer_class'] = self.serializer_class
        return (name, path, args, kwargs)

    def from_db_value(self, value, expression, connection, context):
        """
        Convert database value to Python object.
        """
        return self.to_python(value)

    def value_to_string(self, obj):
        """
        Serialize value of this field in the given model object.

        Note: Doesn't really return a string, but rather serialized
        data of the field value, i.e. dict or list.

        :type obj: models.Model
        :rtype: dict|list
        """
        value = self.value_from_object(obj)
        return self._serialize(value)

    def get_prep_value(self, value):
        """
        Convert Python object to database value.
        """
        if value is None:
            return None
        serialized = self._serialize(value)
        dumped = self.serializer.dump(serialized)
        return super(_Serialized, self).get_prep_value(dumped)

    def to_python(self, value):
        """
        Convert serialized value to Python object.

        Note: Given value might already be a Python object (e.g. when
        called from the `~django.db.models.Field.clean` method).
        """
        if value is None or isinstance(value, self._poly_instance_type):
            return value
        if isinstance(value, (dict, list)):
            # No need to load, since the value is already in the
            # intermediary dict/list format.  This happens when
            # deserializing objects from a stream with
            # `django.core.serializers.deserialize`.
            loaded = value
        else:
            loaded = self.serializer.load(value)
        return self._deserialize(loaded)

    def validate(self, value, model_instance):
        """
        Validate a value of the field.
        """
        serialized = (self.serializer.dump(self._serialize(value))
                      if value is not None else None)
        super(_Serialized, self).validate(serialized, model_instance)


class _SingleSerialized(_Serialized):
    _poly_default = None
    _poly_instance_type = Dictable

    def _serialize(self, value):
        return self.serializer.serialize_object(value)

    def _deserialize(self, serialized_value):
        return self.serializer.deserialize_object(serialized_value)


class _ListSerialized(_Serialized):
    _poly_default = ObjectList
    _poly_instance_type = ObjectList

    def _serialize(self, value):
        return self.serializer.serialize_object_list(value)

    def _deserialize(self, serialized_value):
        return self.serializer.deserialize_object_list(serialized_value)

    def contribute_to_class(self, cls, name, private_only=False,
                            virtual_only=models.NOT_PROVIDED):
        super(_Serialized, self).contribute_to_class(
            cls, name, private_only=private_only, virtual_only=virtual_only)
        list_type = self._poly_instance_type
        base_attr = getattr(cls, name, None)
        assert isinstance(base_attr, DeferredAttribute)
        setattr(cls, name, PolyListAttribute(name, base_attr, list_type))


class PolyListAttribute(object):
    def __init__(self, field_name, base_attr, list_type):
        self.field_name = field_name
        self.base_attr = base_attr
        self.list_type = list_type

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        return self.base_attr.__get__(instance, cls)

    def __set__(self, instance, value):
        if isinstance(value, list) and not isinstance(value, self.list_type):
            value = self.list_type(value)
        instance.__dict__[self.field_name] = value


class _JsonSerializedTextField(models.Field):
    default_serializer_class = JsonSerializer

    def get_internal_type(self):
        return "TextField"

    def formfield(self, **kwargs):
        kwargs.setdefault('widget', forms.Textarea)
        return super(_JsonSerializedTextField, self).formfield(**kwargs)


class PolyField(_SingleSerialized, _JsonSerializedTextField):
    description = _("Polymorphic object")


class PolyListField(_ListSerialized, _JsonSerializedTextField):
    description = _("Polymorphic object list")
