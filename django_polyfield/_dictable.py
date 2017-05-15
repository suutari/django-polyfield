import abc

import six


class Dictable(six.with_metaclass(abc.ABCMeta, object)):
    @classmethod
    def from_dict(cls, data):
        """
        Create an instance from given dictionary.

        :type data: dict
        :rtype: cls
        """
        return cls(**data)

    @abc.abstractmethod
    def to_dict(self):
        """
        Convert this instance to a dictionary.

        :rtype: dict
        """
        return {}

    def __eq__(self, other):
        return type(self) == type(other) and self.to_dict() == other.to_dict()

    def __repr__(self):
        items = sorted(self.to_dict().items())
        kwargs_str = ', '.join('{}={!r}'.format(k, v) for (k, v) in items)
        return '{}({})'.format(type(self).__name__, kwargs_str)
