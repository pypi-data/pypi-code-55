import criterion
import pandas as pd
import numpy as np
from sklearn import ensemble, model_selection, metrics, datasets, tree
import graphviz
import matplotlib.pyplot as plt
from ddop.metrics.costs import calc_avg_costs
from ddop.datasets.load_datasets import load_data
from ddop.newsvendor import RandomForestNewsvendor
from ddop.newsvendor import DecisionTreeNewsvendor
from sklearn.model_selection import train_test_split

"""data = load_data("yaz_steak.csv")
X = data.iloc[:,0:24]
Y = data.iloc[:,24]
cu,co = 15,10
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25)
mdl = RandomForestNewsvendor(max_depth=5, cu=cu, co=co, random_state=0)
mdl = DecisionTreeNewsvendor(max_depth=5, cu=cu, co=co, random_state=0)
mdl.fit(X_train, Y_train)
y_pred = mdl.predict(X_test)
costs = calc_avg_costs(Y_test, y_pred, cu, co)"""

data_x = {'AGE': [91, 42, 29, 94, 85], 'TAX': [384, 223, 280, 666, 384]}
data_y = {'Y1': [19, 21, 24, 13, 18], 'Y2': [19, 21, 24, 13, 18]}

data_x = {'AGE': [1, 2, 3, 4, 5], 'TAX': [10, 9, 8, 7, 6]}
data_y = {'Y1': [11, 12, 13, 14, 15], 'Y2': [20,19,18,17,16]}

x = pd.DataFrame(data_x)
y = pd.DataFrame(data_y)

cu = [5.5,3.5]
co = 1

tree_reg = tree.DecisionTreeRegressor(max_depth=2)
#tree_reg = ensemble.RandomForestRegressor(max_depth=2)
#tree_reg = RandomForestNewsvendor(max_depth=2, cu=2, co=1)
#tree_reg = DecisionTreeNewsvendor(max_depth=5, cu=cu, co=co)
tree_reg.fit(x, y)

'''fn=np.array(['AGE', 'TAX'])
cn=np.array(['Y1','Y2'])
fig, axes = plt.subplots(nrows = 1,ncols = 1,figsize = (4,4), dpi=800)
tree.plot_tree(tree_reg.estimators_[0],
               feature_names = fn,
               class_names=cn,
               filled = True);
fig.savefig('rf_individualtree.png')'''

# Compare visually
dot_data = tree.export_graphviz(tree_reg.estimators_[0], out_file=None, feature_names=x.columns)
graph = graphviz.Source(dot_data)





