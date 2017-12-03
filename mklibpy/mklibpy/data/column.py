__author__ = 'Michael'


class Column(list):
    def __init__(self, name, row):
        list.__init__(self, row)
        self.name = name

    def __repr__(self):
        return repr(self.name) + ": " + list.__repr__(self)

    # --- Custom functions ---

    def sum(self):
        result = 0
        for value in self:
            if value is None:
                continue
            result += value
        return result

    def count(self):
        count = 0
        for value in self:
            if value is None:
                continue
            count += 1
        return count

    def average(self):
        return float(self.sum()) / self.count()
