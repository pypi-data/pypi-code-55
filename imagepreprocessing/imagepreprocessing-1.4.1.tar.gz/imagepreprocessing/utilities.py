import os
import pickle
import itertools 

from imagepreprocessing.file_operations import __read_from_file, __write_to_file

# utilities
def train_test_split(train_x, train_y, test_size=0.2, save_path=None):
    """
    Splits train and test sets from numpy array

    # Arguments:
        train_x: taining data
        train_y: labels of the training data
        test_size (0.2): size of the test set to split
        save_path (None): save path for for seperated data

    # Returns 
        splitted train and test data
        train_x, train_y, test_x, test_y
    """

    new_train_x = []
    new_train_y = []
    
    test_x = []
    test_y = []

    if(len(train_x) != len(train_y)):
        raise ValueError("x and y sizes does not match")
    
    data_count = len(train_x)
    train_percent = int((data_count * test_size))

    new_train_x = train_x[train_percent:]
    new_train_y = train_y[train_percent:]
    
    test_x = train_x[:train_percent]
    test_y = train_y[:train_percent]

    print("\ntest x: {0} test y: {1}".format(len(test_x),len(test_x)))
    print("train x: {0} train y: {1}".format(len(new_train_x),len(new_train_y)))

    # save
    if(save_path != None):
        with open(save_path + "_x_train.pkl", "wb") as file:
            pickle.dump(new_train_x, file, protocol=pickle.HIGHEST_PROTOCOL)
            print("\nfile saved -> {0}{1}".format(save_path,"_x_train.pkl"))

        with open(save_path + "_y_train.pkl", "wb") as file:
            pickle.dump(new_train_y, file, protocol=pickle.HIGHEST_PROTOCOL)
            print("file saved -> {0}{1}".format(save_path,"_y_train.pkl"))
        
        with open(save_path + "_x_test.pkl", "wb") as file:
            pickle.dump(test_x, file, protocol=pickle.HIGHEST_PROTOCOL)
            print("file saved -> {0}{1}".format(save_path,"_x_test.pkl"))

        with open(save_path + "_y_test.pkl", "wb") as file:
            pickle.dump(test_y, file, protocol=pickle.HIGHEST_PROTOCOL)
            print("file saved -> {0}{1}\n".format(save_path,"_y_test.pkl"))
        
    return new_train_x, new_train_y, test_x, test_y


def create_confusion_matrix(predictions, actual_values, class_names=None, one_hot=False, normalize=False):
    """ 
    Creates a confusion matrix

    # Arguments:
        predictions: list of predicted numerical class labels of each sample ex:[1,2,5,3,1]
        actual_values: list of actual numerical class labels of each sample ex:[1,2,5,3,1] or onehot encoded [[0,0,1],[1,0,0],[0,1,0]]
        class_names (None): names of classes that will be drawn, if you want only the array and not the plot pass None (matplotlib required)
        one_hot (False): if labels are one hot formatted use this
        normalize (False): normalizes the values of the matrix

    # Retruns:
        A numpy array of confusion matrix 
    """
    from sklearn.metrics import confusion_matrix
    import numpy as np

    # decode one hot
    if(one_hot):
        labels = []
        for one_hot_value in actual_values:
            for index,value in enumerate(one_hot_value):
                if(value == 1):
                    labels.append(index)
        actual_values = labels

    # create confusion matrix
    cnf_matrix = confusion_matrix(actual_values, predictions)

    if(normalize):
        cnf_matrix = cnf_matrix.astype('float') / cnf_matrix.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Not Normalized confusion matrix')
    
    print("xlabel: True label\nylabel: predicted label")
    print(cnf_matrix)

    # plot the matrix
    if(class_names):
        import matplotlib.pyplot as plt

        title='Confusion matrix'
        cmap=plt.cm.Blues

        plt.imshow(cnf_matrix, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(class_names))
        plt.xticks(tick_marks, class_names, rotation=45)
        plt.yticks(tick_marks, class_names)

        
        thresh = cnf_matrix.max() / 2.
        for i, j in itertools.product(range(cnf_matrix.shape[0]), range(cnf_matrix.shape[1])):
            plt.text(j, i, cnf_matrix[i, j],horizontalalignment="center",color="white" if cnf_matrix[i, j] > thresh else "black")
        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.show()

    return cnf_matrix
