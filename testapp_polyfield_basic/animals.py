from django_polyfield import Dictable


class Animal(Dictable):
    def __init__(self, name):
        self.name = name

    def to_dict(self):
        inner = super(Animal, self).to_dict()
        return dict(inner, name=self.name)


class Bird(Animal):
    def __init__(self, name, sex):
        assert isinstance(sex, str) and sex in ('f', 'm')
        super(Bird, self).__init__(name)
        self.sex = sex

    def to_dict(self):
        return dict(super(Bird, self).to_dict(), sex=self.sex)


class Worm(Animal):
    def __init__(self, name):
        super(Worm, self).__init__(name)
        self.age = 0

    def set_age(self, age):
        assert isinstance(age, int) and age >= 0
        self.age = age

    def to_dict(self):
        return dict(super(Worm, self).to_dict(), age=self.age)

    @classmethod
    def from_dict(cls, data):
        instance = cls(name=data['name'])
        instance.set_age(data.get('age', 0))
        return instance
