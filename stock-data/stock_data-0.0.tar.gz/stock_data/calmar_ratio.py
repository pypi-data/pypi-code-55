import ffn as f


# Defining a class
class calmar_ratio:
    
    def __init__(self, stock, start_date, end_date):
        self.stock = stock
        self.start_date = start_date
        self.end_date = end_date

    def calculate_calmar_ratio(self):
        data = f.get(self.stock, start=self.start_date, end=self.end_date)
        calmar_ratio = f.calc_calmar_ratio(data)
        calmar_ratio = round(calmar_ratio.mean(), 2)
        print (calmar_ratio)
