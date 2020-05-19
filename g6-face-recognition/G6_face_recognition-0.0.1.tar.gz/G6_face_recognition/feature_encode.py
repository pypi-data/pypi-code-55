# USAGE
# python encode_faces1.py --dataset dataset --encodings encodings.pickle

# import the necessary packages

import dlib
import scipy.misc
import numpy as np

global jpeg
global global_frame
face_detector = dlib.get_frontal_face_detector()


shape_predictor = dlib.shape_predictor("encodingModel/Face_model/shape_predictor.dat")


face_recognition_model = dlib.face_recognition_model_v1('encodingModel/Face_model/face_recognition_model.dat')



def engroup(path_to_image):
    try:
        image = scipy.misc.imread(path_to_image)

        detected_faces = face_detector(image, 1)  # 1 is scaleFactor
        # If you begin with the smaller figure, your scale factor will be less than one. If you begin with the larger figure, your scale factor will be greater than one.

        shapes_faces = [shape_predictor(image, face) for face in detected_faces]

        return [np.array(face_recognition_model.compute_face_descriptor(image, face_pose, 1))
                for face_pose in shapes_faces]
    except Exception as e:
        # print("error =", e)
        return []
