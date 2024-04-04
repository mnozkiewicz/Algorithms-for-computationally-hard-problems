class ListSet(list):
    def __init__(self, *args, idx_of=None):
        super(ListSet, self).__init__(*args)
        if idx_of:
            self.idx_of = idx_of.copy()
        else:
            self.idx_of = {item: i
                           for (i, item) in enumerate(self)}

    def add(self, item):
        if item not in self.idx_of:
            super(ListSet, self).append(item)
            self.idx_of[item] = len(self) - 1

    def append(self, item):
        self.add(item)

    def copy(self):
        return ListSet(self, idx_of=self.idx_of)

    def list(self):
        return super(ListSet, self).copy()

    def __iadd__(self, items):
        for item in items:
            self.add(item)
        return self

    def remove(self, element):
        try:
            position = self.idx_of.pop(element)
        except:
            raise (KeyError(element))

        last_item = super(ListSet, self).pop()
        if position != len(self):
            self[position] = last_item
            self.idx_of[last_item] = position

    def pop(self, i=-1):
        item = self[i]
        self.remove(item)
        return item

    def __contains__(self, item):
        return item in self.idx_of

    def _str_body(self):
        return ", ".join(repr(item) for item in self)

    def __repr__(self):
        return "ListSet([" + self._str_body() + "])"

    def __str__(self):
        if self:
            return "{" + self._str_body() + "}"
        else:
            return "ListSet()"
