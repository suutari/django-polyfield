import base64

from six.moves import cPickle

from django_polyfield.serialization import BasicSerializer


class PickleSerializer(BasicSerializer):
    def __init__(self, object_type=None, type_key='T', data_key='D'):
        super(PickleSerializer, self).__init__(object_type, type_key, data_key)

    def dump(self, data):
        return base64.b64encode(cPickle.dumps(data)).decode('ascii')

    def load(self, serialized_data):
        return cPickle.loads(base64.b64decode(serialized_data.encode('ascii')))
