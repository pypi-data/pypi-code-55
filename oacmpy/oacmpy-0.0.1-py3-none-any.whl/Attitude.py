class Attitude:
    def __init__(self, date, attitude):
        self.date = date
        self.attitude = attitude

    def get_date(self):
        return self.date

    def get_quaternion(self):
        return [self.attitude[0], self.attitude[1], self.attitude[2], self.attitude[3]]
