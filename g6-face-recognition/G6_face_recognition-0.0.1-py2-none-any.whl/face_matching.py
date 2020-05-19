import os
from G6_face_recognition.feature_encode import *
import  pickle, numpy as np, re


def face_recg(test_db_model_path,image):

            data = pickle.loads(open(test_db_model_path, "rb").read())
            # [INFO] loading encodings...
            process_this_frame = True
            face_encodings = data["encodings"]
            names = data["names"]
            face_name = match_thread(face_encodings,names,image)
            return face_name




def match_thread(face_encodings,names,face_image):
        face_encodings_in_image = engroup(face_image)
        if len(face_encodings_in_image) >0:
            match = find_match(face_encodings, names, face_encodings_in_image[0])
            return match
        else:
            return "unmatch"




def compare_face_encodings(known_faces, face):
    val = (np.linalg.norm(known_faces - face, axis=1))  # <= tolerance)
    return val


def find_match(known_faces, names, face_encodings_in_image):
    avg_valuelist = []
    min_valuelist = []
    for faces in known_faces:
        matches = compare_face_encodings(faces, face_encodings_in_image)
        avg_value = np.mean(matches)
        min_value = min(matches)
        avg_valuelist.append(avg_value)
        min_valuelist.append(min_value)

    min_avg = avg_valuelist.index(min(avg_valuelist))
    min_value = min_valuelist[min_avg]

    if min_value < 0.43:
        return names[min_avg]
    else:
        return "unmatch"