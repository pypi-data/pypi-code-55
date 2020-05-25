import ffn as f


# Defining a class
class cagr_ratio:
    
    def __init__(self, stock, start_date, end_date):
        self.stock = stock
        self.start_date = start_date
        self.end_date = end_date

    def calculate_cagr_ratio(self):
        data = f.get(self.stock, start=self.start_date, end=self.end_date)
        cagr = f.calc_cagr(data)
        cagr = round(cagr.mean(), 2)
        print (cagr)
