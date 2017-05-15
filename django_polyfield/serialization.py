import abc
import json
from importlib import import_module

import six

from ._list import ObjectList


class Serializer(six.with_metaclass(abc.ABCMeta, object)):
    """
    Interface for serializers.
    """

    @abc.abstractmethod
    def dump(self, data):
        """
        Dump data to serialized format.

        :type data: dict|list
        :rtype: Any
        """

    @abc.abstractmethod
    def load(self, serialized_data):
        """
        Load data from serialized format.

        :type serialized_data: Any
        :rtype: dict|list
        """

    @abc.abstractmethod
    def serialize_object(self, value):
        """
        Serialize object to a dictionary.

        :type value: Any
        :rtype: dict
        """

    @abc.abstractmethod
    def serialize_object_list(self, values):
        """
        Serialize object list to a list of dicts.

        :type value: ObjectList
        :rtype: list[dict]
        """

    @abc.abstractmethod
    def deserialize_object(self, data):
        """
        Deserialize an object from a dict.

        :type data: dict
        :rtype: Any
        """

    @abc.abstractmethod
    def deserialize_object_list(self, data):
        """
        Deserialize a ObjectList from a list of dicts.

        :type data: list[dict]
        :rtype: ObjectList
        """


class BasicSerializer(Serializer):
    def __init__(self, object_type=None, type_key='type', data_key='data'):
        self.object_type = object_type
        self.type_key = type_key
        self.data_key = data_key

    def serialize_object(self, value):
        self.check_type(value)
        return self.dictify(value)

    def serialize_object_list(self, values):
        if not isinstance(values, ObjectList):
            raise TypeError('Value is not a ObjectList. (It is {})'.format(
                type(values).__name__))
        for value in values:
            self.check_type(value)
        return [self.dictify(value) for value in values]

    def deserialize_object(self, data):
        return self.undictify(data)

    def deserialize_object_list(self, data):
        return ObjectList(self.undictify(x) for x in data)

    def dictify(self, value):
        type_string = save_class(type(value))
        data = value.to_dict()
        return {self.type_key: type_string, self.data_key: data}

    def undictify(self, data):
        cls = load_class(data[self.type_key])
        return cls.from_dict(data[self.data_key])

    def check_type(self, value):
        if self.object_type and not isinstance(value, self.object_type):
            raise TypeError('Value is not instance of {}: {!r}'.format(
                self.object_type.__name__, value))


class DataSerializer(BasicSerializer):
    def dump(self, data):
        return data

    def load(self, serialized_data):
        return serialized_data


class JsonSerializer(BasicSerializer):
    def dump(self, data):
        return json.dumps(data, sort_keys=True, separators=(',', ':'))

    def load(self, serialized_data):
        return json.loads(serialized_data)


def save_class(cls):
    """
    Save given class as a string.

    :type cls: type
    :rtype: str
    """
    return '{0.__module__}.{0.__name__}'.format(cls)


def load_class(string):
    """
    Load the class from given string.

    :type string: str
    :rtype: type
    """
    (class_module_name, class_name) = string.rsplit('.', 1)
    module = import_module(class_module_name)
    return getattr(module, class_name)
