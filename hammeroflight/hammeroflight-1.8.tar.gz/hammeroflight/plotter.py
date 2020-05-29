import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')

# __1.6__


def testplot(yt, pred):
    '''
    Author: Aru Raghuvanshi

    This function plots Predictions against Truth Values
    of the Algorithm. Best used for Regression Models.

    Arguments: truth, pred
    Returns: Plot

    '''
    import matplotlib.pyplot as plt
    plt.style.use('seaborn')

    xaxis = range(1, yt.shape[0] + 1)
    plt.figure(figsize=(15, 6))
    plt.scatter(xaxis, yt, color='green', label='Truth Data', marker='o')
    plt.plot(xaxis, pred, color='limegreen', label='Prediction')
    plt.xlabel('Test Observations', fontsize=14)
    plt.ylabel('Predictions', fontsize=14)
    plt.title('Truth Vs Predicted', fontsize=16)
    plt.legend(fontsize=15, loc=4)
    plt.show()

# ======================== FITTING PLOT =========================== ]


# __1.4.3__


def fittingplot(clf, a, b):

    '''
    Author: Aru Raghuvanshi

    This functions takes a single feature and target variable, and plots
    the regression line on that  data to see the fit of the model. The shapes
    of input data should X.shape=(abc,1) and y.shape=(abc, ).

    Argument: estimator, X, y
    Returns: Plot
    '''
    import numpy as np
    import matplotlib.pyplot as plt
    plt.style.use('seaborn')

    a = np.asarray(a).reshape(-1, 1)

    X_grid = np.arange(min(a), max(a), 0.01)
    X_grid = X_grid.reshape((len(X_grid), 1))

    plt.figure(figsize=(14, 6))
    plt.scatter(a, b, color=np.random.rand(3,))   # color=np.random.rand(3,) - to test for 1.4.2
    clf.fit(a, b)
    plt.plot(X_grid, clf.predict(X_grid), color='black')

    plt.title('Fitting Plot', fontsize=16)
    plt.xlabel('Predictor Feature', fontsize=14)
    plt.ylabel('Target Feature', fontsize=14)

    plt.show()





# ======================== FORECAST PLOT =========================== ]

# __1.6.2__


def plot_forecast(true, pred):

    '''
    Author: Aru Raghuvanshi

    This function plots the graph of the Truth values
    and Predicted values of a predictive model and
    visualizes in the same frame. The truth values
    and pred value sizes should be same and both
    should be sharing the same x-axis.


    Arguments: truth value, predicted value
    Returns: Plot

    '''

    import matplotlib.pyplot as plt
    plt.style.use('seaborn')

    plt.figure(figsize=(15, 6))
    plt.plot(true, color='b', label='Test')
    plt.plot(pred, color=np.random.rand(3, ), label='Predicted')
    plt.xlabel('Variable', fontsize=16)
    plt.ylabel('Target', fontsize=16)
    plt.title('Truth v/s Prediction Chart', fontsize=16)
    plt.legend()
    plt.show()



# ===================================== VARIABLE PLOTTER =======================

# _1.7.5__ TO BE ADDED TO 1.8

def variable_plotter(a, b, labela, labelb, title=None, xlabel=None, ylabel=None, bar=True):
    '''
    Author: Aru Raghuvanshi

    The functions plots graph between two variables.
    bar = True by default, else Line
    title, xlabel, ylabel: Pass as type str.

    Returns: Plot
    '''

    s = []
    t = []
    s.append(a)
    t.append(b)
    pr = pd.DataFrame(list(zip(s, t)), columns=[labela, labelb])
    if bar == True:
        plt.figure(figsize=(12, 5))
        pr.plot(kind='bar', figsize=(10, 6))
        plt.title(title, fontsize=15)
        plt.xlabel(xlabel, fontsize=15)
        plt.ylabel(ylabel, fontsize=15)

    else:
        plt.figure(figsize=(12, 5))
        pr.plot(kind='line', figsize=(10, 6))
        plt.title(title, fontsize=15)
        plt.xlabel(xlabel, fontsize=15)
        plt.ylabel(ylabel, fontsize=15)





# ============================= CNN HISTORY PLOTTER =================================


# To be added to 1.7.5

def historyplot(model):
    '''
    Author: Aru Raghuvanshi

    Plots the evaluation metrics of CNN.
    model.history.history
    Where the eval metrics are val_loss
    or val_accuracy, or loss or accuracy

    Returns: Plot
    '''
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set()

    model.history.history = pd.DataFrame(model.history.history)

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16, 7))
    ax1.plot(model.history.history['val_accuracy'], marker='+', color='dodgerblue')
    ax1.set_title('Test Accuracy by Epoch', fontsize=16)
    ax1.set_xlabel('Epoch', fontsize=16)
    ax1.set_ylabel('Accuracy', fontsize=14)
    ax1.set_ylim(0.8, 1)
    ax2.plot(model.history.history['loss'], label='Training loss', color='deepskyblue')
    ax2.plot(model.history.history['val_loss'], label='Testing loss', color='coral')
    ax2.set_title('Loss Reduction by Epoch', fontsize=16)
    ax2.set_xlabel('Epoch', fontsize=16)
    ax2.set_ylabel('Accuracy', fontsize=14)
    ax2.set_ylim(0, 1)
    ax2.legend();