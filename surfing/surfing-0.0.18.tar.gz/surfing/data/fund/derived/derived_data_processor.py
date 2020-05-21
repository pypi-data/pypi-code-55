from .fund_score_processor import FundScoreProcessor
from .fund_indicator_processor import FundIndicatorProcessor
from .derived_index_val import IndexValProcess

class DerivedDataProcessor(object):
    def __init__(self):
        self.fund_indicator_processor = FundIndicatorProcessor()
        self.fund_score_processor = FundScoreProcessor()
        self.index_val_processor = IndexValProcess()
        self.updated_count = {}

    def process_all(self, start_date, end_date):
        failed_tasks = []

        failed_tasks.extend(self.fund_indicator_processor.process(start_date, end_date))
        failed_tasks.extend(self.fund_score_processor.process(start_date, end_date))
        failed_tasks.extend(self.index_val_processor.process(start_date, end_date))
        
        for key, value in self.fund_indicator_processor.updated_count.items():
            if key not in self.updated_count:
                self.updated_count[key] = value
            else:
                self.updated_count[key] += value

        for key, value in self.fund_score_processor.updated_count.items():
            if key not in self.updated_count:
                self.updated_count[key] = value
            else:
                self.updated_count[key] += value

        for key, value in self.index_val_processor.updated_count.items():
            if key not in self.updated_count:
                self.updated_count[key] = value
            else:
                self.updated_count[key] += value

        return failed_tasks

if __name__ == '__main__':
    ddp = DerivedDataProcessor()
    # start_date = '20200430'
    start_date = '20200506'
    end_date = '20200506'
    ddp.fund_score_processor.process(start_date, end_date)
