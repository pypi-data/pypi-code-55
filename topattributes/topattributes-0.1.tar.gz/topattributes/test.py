from TopAttributes import Topvariables
import pandas as pd

data = pd.read_csv('train.csv')
dep = 'Survived'
Topvariables.correlation