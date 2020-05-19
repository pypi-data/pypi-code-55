# import the necessary packages
from imutils import paths
import pickle
import os
from G6_face_recognition.feature_encode import *


def face_test_model(train_db_path,train_db_model_path):
    directory_list = list()
    for root, dirs, files in os.walk(
            train_db_path,
            topdown=False):
        for name in dirs:
            directory_list.append(os.path.join(root, name))


    face_names=[]
    face_name_encodings=[]
    invalid_image=False
    for directory in directory_list:
        # grab the paths to the input images in our dataset
        paths_to_images = list(paths.list_files(os.path.join(directory)))
        # initialize the list of face_name_encodings and face_names
        face_encodings = []
        name = directory.split(os.path.sep)[-1]
    

        # Encode the images located in the folder to thier respective numpy arrays
        invalid_image=False
        for path_to_image in paths_to_images:
            face_encodings_in_image = engroup(path_to_image)
            if len(face_encodings_in_image) == 0:
                invalid_image=True
            else:
                invalid_image = False
                face_encodings.append(face_encodings_in_image[0])



        if invalid_image == True :
            invalid_image=False
        else:
            face_names.append(name)
            face_name_encodings.append(face_encodings)





    # "[INFO] serializing encodings..."
    data = {"encodings": face_name_encodings, "names": face_names}
    f = open(train_db_model_path, "wb")
    f.write(pickle.dumps(data))
    f.close()
    return face_names




















