class State:
    def __init__(self, date, states):
        self.date = date
        self.states = states

    def get_date(self):
        return self.date

    def get_state(self):
        return self.states

    def get_position(self):
        return [self.states[0], self.states[1], self.states[2]]
