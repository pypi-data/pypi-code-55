import os
import random
import pickle
import itertools 
from shutil import copyfile

from imagepreprocessing.file_operations import __read_from_file, __write_to_file

# keras functions

def create_training_data_keras(source_path, save_path = None, image_size = (224,224), percent_to_use = 1, validation_split = 0, normalize = 255, grayscale = False, one_hot = True, shuffle = True, convert_array_and_reshape = True, files_to_exclude = [".DS_Store",""]):
    """
    Creates train ready data for classification from image data
    Takes all the image directories alphabetically in a main directory 

    # Arguments:
        source_path: source path of the images see input format
        save_path (None): save path for clean training data 
        image_size ((224,224)): size of the images for resizing tuple of 2 ints or a single int
        percent_to_use (1): percentage of data that will be used
        validation_split (0.2): splits validation data with given percentage give 0 if you don't want validation split
        normalize (255): (pass None or False if you don't want normalization) divides all images by 255 this normalizes images if pixel values are maximum of 255 if it is different change this value   
        grayscale (False): converts images to grayscale
        one_hot (True): makes one hot encoded y train if True if not uses class indexes as labels
        shuffle (True): shuffle the data
        convert_array_and_reshape (True): converts list to numpy array and reshapes images at the and if True
        files_to_exclude ([".DS_Store",""]): list of file names to exclude in the image directory (can be hidden files)

    # Returns:
        List or numpy array of train data optionally validation data
        if validation_split is 0 -> x, y
        if validation_split is not 0 -> x, y, x_val, y_val

    # Save:
        Saves x train and y train optionally validation x and y 
        Save format is .pkl (pickle data)
        If you want you can prevent saveing the file by passing None as save_path

    # Input format:
        source_path = some_dir
        
        /some_dir
        ├──/class1
            ├──img1.jpg
            ├──img2.jpg
        ├──/class2
            ├──img1.jpg

    # Output format:
        save_path = save/food_data

        save/food_data_x_train.pkl
        save/food_data_y_train.pkl   
        save/food_data_x_validation.pkl
        save/food_data_y_validation.pkl   
        
    # Example:
        ``python
            source_path = "C:\\Users\\can\\datasets\\deep_learning\\food-101\\only3"
            save_path = "C:\\Users\\can\\Desktop\\food10class1000sampleeach"
            create_training_data_keras(source_path, save_path, image_size = 299, validation_split=0.1, percent_to_use=0.1, grayscale = True, files_to_exclude=["excludemoe","hi.txt"])
        ``                      
    """

    import numpy as np
    import cv2

    # image_size parsing
    if(type(image_size) == tuple):
        if(len(image_size) == 2 and type(image_size[0]) == int and type(image_size[1]) == int):
            img_width = image_size[0]
            img_height = image_size[1]
        else:
            raise ValueError("image_size tuple should have 2 int values")
    elif(type(image_size) == int):
        img_width = image_size
        img_height = image_size
    else:
        raise ValueError("image_size should be an int or a tuple with 2 int values")

    if(img_width < 1 or img_height < 1):
        raise ValueError("image_size should be bigger than 0")


    # raise error on wrong percentage
    if(validation_split < 0 or validation_split > 1):
        raise ValueError("Validation_split should be between 0 and 1")

    


    x = []
    y = [] 
    x_val = []
    y_val = []

    CATEGORIES = os.listdir(source_path)  # get all file names from main dir
    CATEGORIES.sort()                     # sort the directories

    # remove excluded files
    for exclude in files_to_exclude:
        if exclude in CATEGORIES: 
            CATEGORIES.remove(exclude)
    


    # loop in the main directory
    for category_index, category in enumerate(CATEGORIES):

        path = os.path.join(source_path, category)
        number_of_categories = len(CATEGORIES)
        index_of_category = CATEGORIES.index(category)

        # if wrong directory style given raise error
        try:
            images = os.listdir(path)
        except NotADirectoryError as e:
            raise NotADirectoryError(e,"""
        Your dataset should look like this
        /source_path
        |---/dir1(class1)
            |---img1.jpg
            |---img2.jpg
        |---/dir2(class2)
            |---img1.jpg
            ... 
        """)

        # raise error on wrong percentage
        if(percent_to_use <= 0 or percent_to_use > 1):
            raise ValueError("Percentage should be between 0 and 1")
        elif(int(percent_to_use * len(images)) == 0):
            raise ValueError("Percentage is too small for this directory {0}".format(category))
        else:
            stop_index = int(len(images)*percent_to_use)
        
        
        is_there_broken_images = ""
        # loop inside each category folder with itertools for stoping on a percentage
        for image_index, img in enumerate(itertools.islice(images , 0, stop_index)):

            # print percent info
            print("File name: {0} - {1}/{2}  Image:{3}/{4} {5}".format(category, index_of_category+1, number_of_categories, image_index+1, stop_index, is_there_broken_images), end="\r")
            
            # there can be broken images
            try:
                # convert grayscale
                if(grayscale):
                    temp_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                else:
                    temp_array = cv2.imread(os.path.join(path, img)) 

                # resize image
                img_array = cv2.resize(temp_array, (img_width, img_height))   

                # one hot encoding
                if(one_hot):  
                    temp_y = []
                    for i in range(len(CATEGORIES)):
                        if(i == category_index):
                            temp_y.append(1)
                        else:
                            temp_y.append(0)
                    y.append(temp_y)
                # if one hot is not selected use index of the file as label
                else:
                    y.append(index_of_category)  

                x.append(img_array)
            except:
                is_there_broken_images = " ---There are some corrupted images in this directory, skiping those images---"
                pass

        print("")


    if(shuffle):
        print("\n...shuffling...")
        xy = list(zip(x,y))
        random.shuffle(xy)
        x, y = list(zip(*xy))
    

    # validation split
    if(validation_split):
        print("\n...splitting validation...")
        if(int(validation_split * len(images)) == 0):
            raise ValueError("Validation split is too small for this set")

        # split
        train_percent = int(len(x) - (validation_split * len(x)))
        x_val = x[train_percent:]
        y_val = y[train_percent:]
        x = x[:train_percent]
        y = y[:train_percent]

        print("train x: {0} train y: {1}\nvalidation x: {2} validation y: {3}".format(len(x),len(y),len(x_val),len(y_val)))
    else:
        print("\ntrain x: {0} train y: {1}".format(len(x),len(y)))



    # convert array and reshape 
    if(convert_array_and_reshape):
        print("\n...converting train to array...")
        if(grayscale):
            third_dimension = 1
        else:
            third_dimension = 3
    
        x = np.array(x).reshape(-1, img_width, img_height, third_dimension)
        y = np.array(y)

        print("Array converted shape of train x: {0}\nArray converted shape of train y: {1}".format(x.shape,y.shape))

        if(validation_split):
            print("\n...converting validation to array...")
            x_val = np.array(x_val).reshape(-1, img_width, img_height, third_dimension)
            y_val = np.array(y_val)    
            print("Array converted shape of validation x: {0}\nArray converted shape of validation y: {1}".format(x_val.shape,y_val.shape))


    # normalize 
    if(normalize):
        if(convert_array_and_reshape):
            print("\n...normalizing train x...")
            x = x/normalize
            print("Normalized example from train set (x[0][0][0]): {0}".format(x[0][0][0]))
            if(validation_split):
                print("\n...normalizing validation x...")
                x_val = x_val/normalize
                print("Normalized example from validation set (x_val[0][0][0]): {0}".format(x_val[0][0][0]))
        else:
            print("\n...normalizing train x (if normalization is slow use convert_array_and_reshape with normalization)...")
            x = (np.array(x)/normalize).tolist()
            print("Normalized example from train set (x[0][0][0]): {0}".format(x[0][0][0]))
            if(validation_split):
                print("\n...normalizing validation x...")
                x_val = (np.array(x_val)/normalize).tolist()
                print("Normalized example from validation set (x_val[0][0][0]): {0}".format(x_val[0][0][0]))


    # save
    if(save_path != None):
        with open(save_path + "_x_train.pkl", "wb") as file:
            pickle.dump(x, file, protocol=pickle.HIGHEST_PROTOCOL)
            print("\nfile saved -> {0}{1}".format(save_path,"_x_train.pkl"))

        with open(save_path + "_y_train.pkl", "wb") as file:
            pickle.dump(y, file, protocol=pickle.HIGHEST_PROTOCOL)
            print("file saved -> {0}{1}".format(save_path,"_y_train.pkl"))
        
        if(validation_split != 0):
            with open(save_path + "_x_validation.pkl", "wb") as file:
                pickle.dump(x_val, file, protocol=pickle.HIGHEST_PROTOCOL)
                print("file saved -> {0}{1}".format(save_path,"_x_validation.pkl"))

            with open(save_path + "_y_validation.pkl", "wb") as file:
                pickle.dump(y_val, file, protocol=pickle.HIGHEST_PROTOCOL)
                print("file saved -> {0}{1}\n".format(save_path,"_y_validation.pkl"))
        
    if(validation_split):
        return x, y, x_val, y_val
    else:
        return x, y


def make_prediction_from_directory_keras(images_path, keras_model_path, image_size = (224,224), print_output=True, model_summary=True, show_images=False, grayscale = False, files_to_exclude = [".DS_Store",""]):
    """
    Reads test data from directory resizes it and makes prediction with using a keras model

    # Arguments:
        images_path: source path of the test images see input format
        keras_model_path: path of the keras model 
        img_size (224): size of the images for resizing
        print_output (True): prints output
        model_summary (True): shows keras model summary 
        show_images (False): shows the predicted image
        grayscale (False): converts images to grayscale
        files_to_exclude ([".DS_Store",""]): list of file names to exclude in the image directory (can be hidden files)

    # Returns:
        Prediction results in a list
    
    # Input format:
        images_path = some_dir
        
        /some_dir
            ├──img1.jpg
            ├──img2.jpg
    """

    import warnings
    warnings.filterwarnings("ignore")

    import matplotlib.pyplot as plt
    import numpy as np
    import keras
    import cv2

    # image_size parsing
    if(type(image_size) == tuple):
        if(len(image_size) == 2 and type(image_size[0]) == int and type(image_size[1]) == int):
            img_width = image_size[0]
            img_height = image_size[1]
        else:
            raise ValueError("image_size tuple should have 2 int values")
    elif(type(image_size) == int):
        img_width = image_size
        img_height = image_size
    else:
        raise ValueError("image_size should be an int or a tuple with 2 int values")


    test_images = []
    test_image_names = []

    images = os.listdir(images_path)
    images.sort()

    # remove excluded files
    for exclude in files_to_exclude:
        if exclude in images: 
            images.remove(exclude)

    # load model
    model = keras.models.load_model(keras_model_path)

    # get all images
    for image in images:
        abs_path = os.path.join(images_path, image)

        try:
            if(grayscale):
                third_dimension = 1
                img_array = cv2.imread(abs_path, cv2.IMREAD_GRAYSCALE)
            else:
                third_dimension = 3
                img_array = cv2.imread(abs_path)

            new_array = cv2.resize(img_array, (img_width, img_height))
            test_images.append(new_array.reshape(-1, img_width, img_height, third_dimension))    
            test_image_names.append(image)
        except:
            pass
    
    # show model summary
    if(model_summary):
        model.summary()

    predictions = []

    for image, name in zip(test_images,test_image_names):
        prediction = model.predict(image)
        prediction_class = np.argmax(prediction)
        predictions.append(prediction_class)
        if(print_output):
            print("{0} : {1}".format(name,prediction_class))

        if(show_images):
            abs_path = os.path.join(images_path, name)
            img = cv2.imread(abs_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgplot = plt.imshow(img)
            plt.show()

    return predictions


def make_prediction_from_array_keras(test_x, keras_model_path, print_output=True, model_summary=True, show_images=False):
    """
    makes prediction with using a keras model

    # Arguments:
        test_x: numpy array of images
        keras_model_path: path of the keras model
        print_output (True): prints output
        model_summary (True): shows keras model summary 
        show_images (False): shows the predicted image
        grayscale (False): converts images to grayscale
        files_to_exclude ([".DS_Store",""]): list of file names to exclude in the image directory (can be hidden files)

    # Returns:
        Prediction results in a list
    """

    import warnings
    warnings.filterwarnings("ignore")

    import matplotlib.pyplot as plt
    import numpy as np
    import keras
    import cv2

    # load model
    model = keras.models.load_model(keras_model_path)

    # show model summary
    if(model_summary):
        model.summary()

    
    if(type(test_x) == list):
        multi_input_model = True
    else:
        multi_input_model = False

    # add an extra dimension to array since we are iterating over the array the first dimension is disapeares
    if(multi_input_model):
        print("...multi input received reshapeing...")
        new_x = []
        for i in range(test_x[0].shape[0]):
            temp = []
            for test_arr in test_x:
                temp.append(np.expand_dims(test_arr[i], axis=0))
            new_x.append(temp)
        test_x = new_x
    else:
        new_x = []
        for image in test_x:
            new_x.append(np.expand_dims(image, axis=0))
        test_x = new_x

    predictions = []
    for index, image in enumerate(test_x):
        prediction = model.predict(image)
        prediction_class = np.argmax(prediction)
        predictions.append(prediction_class)

        if(print_output):
            print("{0}/{1} -> {2}".format(len(test_x), index, prediction_class))
        else:
            print("{0}/{1}".format(len(test_x),index),end="\r")

        if(show_images):
            try:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                imgplot = plt.imshow(image)
                plt.show()
            except TypeError  as e:
                raise TypeError(e,"""
            input array is not representable as image try with option show_images=False""")

    return predictions