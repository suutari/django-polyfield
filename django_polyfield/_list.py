class ObjectList(list):
    def instances_of(self, cls):
        for value in self:
            if isinstance(value, cls):
                yield value
