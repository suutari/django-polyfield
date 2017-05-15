import pytest
from django.conf import settings

from testapp_polyfield_basic.animals import Bird, Worm


@pytest.mark.django_db
def test_bare_postgres_json_field():
    (objs, bird_b, worm_b) = get_objs()
    assert objs.get(bare_json__name='Bird B').obj == bird_b, (
        "The bare PostgreSQL JSONField works as intended")


@pytest.mark.django_db
def test_contains_lookup():
    (objs, bird_b, worm_b) = get_objs()
    assert objs.get(obj__data__name__contains='Bird B').obj == bird_b, (
        "contains lookup works")


@pytest.mark.django_db
def test_icontains_lookup():
    (objs, bird_b, worm_b) = get_objs()
    assert objs.get(obj__data__name__icontains='bird b').obj == bird_b, (
        "icontains lookup works")


@pytest.mark.django_db
def test_exact_lookup():
    (objs, bird_b, worm_b) = get_objs()
    assert objs.get(obj__data__name='Bird B').obj == bird_b, (
        "exact lookup works")


@pytest.mark.django_db
def test_contained_by_lookup():
    (objs, bird_b, worm_b) = get_objs()
    data_cover = {'name': 'Worm B', 'age': 2, 'bogus': 'extra'}
    cover = {
        'type': 'testapp_polyfield_basic.animals.Worm',
        'data': data_cover,
    }
    assert objs.get(obj__contained_by=cover).obj == worm_b, (
        "contained_by lookup works")
    assert objs.get(obj__data__contained_by=data_cover).obj == worm_b, (
        "contained_by lookup works for the data sub-dictionary")


@pytest.mark.django_db
def test_has_key_lookup():
    (objs, bird_b, worm_b) = get_objs()
    assert objs.filter(obj__data__has_key='age').count() == 20, (
        "has_key lookup works")


@pytest.mark.django_db
def test_has_keys_lookup():
    (objs, bird_b, worm_b) = get_objs()
    assert objs.filter(obj__data__has_keys=['name', 'age']).count() == 20, (
        "has_keys lookup works for matching results")
    assert objs.filter(obj__data__has_keys=['sex', 'age']).count() == 0, (
        "has_keys lookup works for non-matching results")


@pytest.mark.django_db
def test_has_any_keys_lookup():
    (objs, bird_b, worm_b) = get_objs()
    assert objs.filter(obj__data__has_any_keys=['sex', 'age']).count() == 30, (
        "has_any_keys lookup works for matching results")
    assert objs.filter(obj__data__has_any_keys=['bogus']).count() == 0, (
        "has_any_keys lookup works for non-matching results")


# TODO: Tests for PolyJsonListField


def get_objs():
    check_postgres_support()

    from testapp_polyfield_pg.models import PostgresJsonObject

    # Create the objects
    for i in range(0, 10):
        bird = Bird('Bird ' + chr(ord('A') + i), ['f', 'm'][i % 2])
        PostgresJsonObject.objects.create(obj=bird, bare_json=bird.to_dict())
    for i in range(0, 20):
        worm = Worm('Worm ' + chr(ord('A') + i))
        worm.set_age(i + 1)
        PostgresJsonObject.objects.create(obj=worm, bare_json=worm.to_dict())

    # Test instances
    bird_b = Bird('Bird B', 'm')
    worm_b = Worm.from_dict({'name': 'Worm B', 'age': 2})

    return (PostgresJsonObject.objects, bird_b, worm_b)


def check_postgres_support():
    try:
        import psycopg2  # noqa
    except ImportError:
        pytest.skip('psycopg2 is not installed')

    pg_engine = 'django.db.backends.postgresql_psycopg2'
    if settings.DATABASES['default']['ENGINE'] != pg_engine:
        pytest.skip('Django database engine is not psycopg2')
