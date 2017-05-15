import pytest

from django_polyfield import Dictable


class Vehicle(Dictable):
    def __init__(self, speed, **kwargs):
        self.speed = speed
        super(Vehicle, self).__init__(**kwargs)

    def to_dict(self):
        return dict(super(Vehicle, self).to_dict(), speed=self.speed)


class MotorVehicle(Vehicle):
    def __init__(self, power, **kwargs):
        self.power = power
        super(MotorVehicle, self).__init__(**kwargs)

    def to_dict(self):
        return dict(super(MotorVehicle, self).to_dict(), power=self.power)


class Boat(Vehicle):
    def __init__(self, length, **kwargs):
        assert isinstance(length, float)
        self.length = length
        super(Boat, self).__init__(**kwargs)

    def to_dict(self):
        return dict(super(Boat, self).to_dict(), length=self.length)


class MotorBoat(MotorVehicle, Boat):
    pass


def test_from_dict():
    boat = MotorBoat.from_dict(dict(speed=83, power=1123, length=37.2))
    assert isinstance(boat, MotorBoat)
    assert type(boat) == MotorBoat
    assert boat.speed == 83
    assert boat.power == 1123
    assert boat.length == 37.2


def test_to_dict():
    boat = MotorBoat(speed=83, power=1123, length=37.2)
    assert boat.to_dict() == {'length': 37.2, 'power': 1123, 'speed': 83}


def test_eq():
    boat1a = MotorBoat(speed=83, power=1123, length=37.2)
    boat1b = MotorBoat(speed=83, power=1123, length=37.2)
    boat2 = MotorBoat(speed=84, power=1123, length=37.2)
    assert boat1a == boat1b
    assert boat1a != boat2
    assert boat2 == boat2


def test_repr():
    boat = MotorBoat(speed=83, power=1123, length=37.2)
    assert repr(boat) == 'MotorBoat(length=37.2, power=1123, speed=83)'


def test_abstractness():
    with pytest.raises(TypeError) as excinfo:
        Dictable()
    assert '{}'.format(excinfo.value) == (
        "Can't instantiate abstract class Dictable "
        "with abstract methods to_dict")
