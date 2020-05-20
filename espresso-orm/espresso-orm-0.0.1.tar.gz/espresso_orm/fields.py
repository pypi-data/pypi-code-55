
class Fields:

    def __init__(self, name="test", required=False, unique=False):
        super().__init__(name, required=False, unique=False)

        self.required = required
        self.unique = unique




class String(Fields):

    def __init__(self, name="test", required=False, unique=False):
        super().__init__(name="test", required=False, unique=False)


class Integer(Fields):

    def __init__(self, name="test", required=False, unique=False):
        super().__init__(name="test", required=False, unique=False)


class Floor(Fields):

    def __init__(self, name="test", required=False, unique=False):
        super().__init__(name="test", required=False, unique=False)


class One2many(Fields):

    def __init__(self, name="test", required=False, unique=False):
        super().__init__(name="test", required=False, unique=False)
