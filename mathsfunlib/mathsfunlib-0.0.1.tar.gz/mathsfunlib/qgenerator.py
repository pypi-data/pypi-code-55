import random
import time
from enum import Enum

MAX_TABLE = 12


class QType(Enum):
    MULTIPLICATION = 1
    XMULTIPLICATION = 2
    DIVISION = 3
    XDIVISION = 4


class Question(object):
    def __init__(self):
        self.qstring = None
        self.answer = None
        self.qtype = None

    def get_answer(self):
        return self.answer

    def get_question(self):
        return self.qstring


class MultiplicationQuestion(Question):
    def __init__(self, x, y):
        super(Question, self).__init__()
        self.qtype = QType.MULTIPLICATION
        self.x = x
        self.y = y
        self.answer = x * y
        self.qstring = "{} x {} = _".format(x, y)

    def __repr__(self):
        return "x = {} y = {} answer = {}".format(self.x, self.y, self.answer)

    def __str__(self):
        return self.qstring


class DivisionQuestion(Question):
    def __init__(self, x, y):
        super(Question, self).__init__()
        self.qtype = QType.DIVISION
        self.x = x
        self.y = y
        self.result = x * y
        self.answer = x
        self.qstring = "{} ÷ {} = _".format(self.result, y)

    def __repr__(self):
        return "x = {} y = {} answer = {}".format(self.x, self.y, self.answer)

    def __str__(self):
        return self.qstring


class XMultiplicationQuestion(Question):
    def __init__(self, x, y):
        super(Question, self).__init__()
        self.qtype = QType.XMULTIPLICATION
        self.x = x
        self.y = y
        self.result = x * y
        side = random.choice(['Left', 'Right'])
        if side == 'Left':
            self.answer = x
            self.qstring = "_ x {} = {}".format(self.y, self.result)
        else:
            self.answer = y
            self.qstring = "{} x _= {}".format(self.x, self.result)

    def __repr__(self):
        return "x = {} y = {} result = {}".format(self.x, self.y, self.result)

    def __str__(self):
        return self.qstring


class XDivisionQuestion(Question):
    def __init__(self, x, y):
        super(Question, self).__init__()
        self.qtype = QType.XDIVISION
        self.x = x
        self.y = y
        self.result = x * y
        side = random.choice(['Left', 'Right'])
        if side == 'Left':
            self.answer = self.result
            self.qstring = "_ ÷ {} = {}".format(self.y, self.x)
        else:
            self.answer = self.y
            self.qstring = "{} ÷ _ = {}".format(self.result, self.x)

    def __repr__(self):
        return "x = {} y = {} result = {}".format(self.x, self.y, self.result)

    def __str__(self):
        return self.qstring


class QGenertor(object):
    def __init__(self, tables_list):
        self.tables_list = tables_list
        self.x = None
        self.y = None

    def get(self):
        self.x = random.choice(range(1, MAX_TABLE))
        self.y = random.choice(self.tables_list)


class MQGenerator(QGenertor):
    def __init__(self, tables_list):
        super(MQGenerator, self).__init__(tables_list)

    def get(self):
        super(MQGenerator, self).get()
        return MultiplicationQuestion(self.x, self.y)


class DQGenerator(QGenertor):
    def __init__(self, tables_list):
        super(DQGenerator, self).__init__(tables_list)

    def get(self):
        super(DQGenerator, self).get()
        return DivisionQuestion(self.x, self.y)


class XMQGenerator(QGenertor):
    def __init__(self, tables_list):
        super(XMQGenerator, self).__init__(tables_list)

    def get(self):
        super(XMQGenerator, self).get()
        return XMultiplicationQuestion(self.x, self.y)


class XDQGenerator(QGenertor):
    def __init__(self, tables_list):
        super(XDQGenerator, self).__init__(tables_list)

    def get(self):
        super(XDQGenerator, self).get()
        return XDivisionQuestion(self.x, self.y)


class_map = {
    QType.MULTIPLICATION: MQGenerator,
    QType.XMULTIPLICATION: XMQGenerator,
    QType.DIVISION: DQGenerator,
    QType.XDIVISION: XDQGenerator
}


def generate_questions(tables, types):
    total_count = len(tables) * 10
    print("total_count: {}".format(total_count))
    for _ in range(total_count):
        qtype = random.choice(types)
        gc = class_map.get(qtype)
        question = gc(tables).get()
        yield question


