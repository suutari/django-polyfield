from django_polyfield.serialization import DataSerializer, JsonSerializer


def test_json_serializer_dump():
    serializer = JsonSerializer()
    dumped = serializer.dump({'hello': 'world'})
    assert dumped == '{"hello":"world"}'


def test_json_serializer_load():
    serializer = JsonSerializer()
    loaded = serializer.load('{"hello":"world"}')
    assert loaded == {'hello': 'world'}


def test_data_serializer_dump():
    serializer = DataSerializer()
    dumped = serializer.dump({'hello': 'world'})
    assert dumped == {'hello': 'world'}


def test_data_serializer_load():
    serializer = DataSerializer()
    loaded = serializer.load({'hello': 'world'})
    assert loaded == {'hello': 'world'}
