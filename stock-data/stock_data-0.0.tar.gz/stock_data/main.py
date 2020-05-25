from value_at_risk import value_at_risk
import datetime 

start_date = datetime.datetime(2019,12,28)
end_date = datetime.date.today()

'''
MSFT = value_at_risk(['MSFT', 'AAPL', 'AMZN'], [0.1, 0.6, 0.3], 100000, start_date, end_date)
MSFT.calculate_value_at_risk()
'''


MSFT = value_at_risk('MSFT', 1.0, 100000, start_date, end_date)
MSFT.calculate_value_at_risk()
