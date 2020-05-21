from .basic_data_part1 import BasicDataPart1
from .basic_data_part2_fund_ret import BasicFundRet

class BasicDataProcessor(object):
    def __init__(self):
        self.basic_data_part1 = BasicDataPart1()
        self.basic_fund_ret = BasicFundRet()
        self.updated_count = {}

    def process_all(self, start_date, end_date):
        failed_tasks = []

        failed_tasks.extend(self.basic_data_part1.process_all(start_date, end_date))
        failed_tasks.extend(self.basic_fund_ret.process_all(end_date))

        for key, value in self.basic_data_part1.updated_count.items():
            if key not in self.updated_count:
                self.updated_count[key] = value
            else:
                self.updated_count[key] += value

        for key, value in self.basic_fund_ret.updated_count.items():
            if key not in self.updated_count:
                self.updated_count[key] = value
            else:
                self.updated_count[key] += value

        return failed_tasks