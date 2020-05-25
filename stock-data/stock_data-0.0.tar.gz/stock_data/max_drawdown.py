import ffn as f


# Defining a class
class max_drawdown:
    
    def __init__(self, stock, start_date, end_date):
        self.stock = stock
        self.start_date = start_date
        self.end_date = end_date

    def calculate_max_drawdown(self):
        data = f.get(self.stock, start=self.start_date, end=self.end_date)
        max_drawdown = f.calc_max_drawdown(data)
        max_drawdown = round(max_drawdown.mean(), 2)
        print (max_drawdown)
