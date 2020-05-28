import os, sys, time, dlib, face_recognition, cv2
import numpy as np
from PIL import Image
import pkg_resources

def facedetection(unknownimage, knownimage, path=None, save_path=None):
    """ Takes an unknown image and looks for faces. """
    haar_xml = pkg_resources.resource_filename(
        'cv2', 
        'data/haarcascade_frontalface_default.xml'
        )
    faces_cascade = cv2.CascadeClassifier(haar_xml)
    unknown_image = os.path.join(path, unknownimage)
    img = cv2.imread(unknown_image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faces_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) != 0 : #If the haar algorithm finds a face, it fill fill the array-> faces!=0
        facerecognition(unknownimage, knownimage, path)

        for (x, y, w, h) in faces: # Draws rectangles around the faces
            cv2.rectangle(img, (x ,y), (x+w ,y+h), (0, 255, 0), 2)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        if save_path != None:
            cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
            filename = time.ctime()
            os.chdir(save_path)
            cv2.imwrite(f'{filename}', cv2image)


def facerecognition(unknownimage, knownimage, path):
    """ This takes an unknown image and compare it with an known image. If the face_recognition deems them to be the same person you will return true """
    if path == None:
        pass #wer're in the same directory as the files
    else:
        file_for_unknown = os.path.join(path, unknownimage)
        file_for_known = os.path.join(path, knownimage)
        unknown = face_recognition.load_image_file(file_for_unknown)
        known = face_recognition.load_image_file(file_for_known)
        unknown_encoding = face_recognition.face_encodings(unknown)[0]
        known_encoding = face_recognition.face_encodings(known)[0]

        result = face_recognition.compare_faces([known_encoding], unknown_encoding)
        return f'The face-recognition test was {result}.', result


def video_facedetect(camera = 0, referense_image = None, path = None, save_path = None, multiple = None):
    """Detects faces in a specified camera-port, takes a referense picture and check them. If no specified path is present, it will look in the current directory,
    likewise if no save_path is specified it will save it into the current directory."""
    haar_xml = pkg_resources.resource_filename(
        'cv2', 
        'data/haarcascade_frontalface_default.xml'
        )
    if path == None:
        directory = os.getcwd()
        os.chdir(directory)
    else:
        os.chdir(path)
    if save_path == None:
        save_path = os.getcwd()
    referense_image_path = os.path.join(path, referense_image)
    if not multiple == None:
        fetchfile(multiple)
    
    faces_cascade = cv2.CascadeClassifier(haar_xml)
    cap = cv2.VideoCapture(camera)
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faces_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) != 0: #If the haar algorithm finds a face, it fill fill the array-> faces!=0
        for (x, y, w, h) in faces: # Draws rectangles around the faces
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    filename = f'{time.ctime()}.png'
    name = os.path.join(save_path, filename)

    cv2.imwrite(name, cv2image)
    #cv2.waitKey()
    if referense_image == None:
        recognition(name, referense_image_path)
    else:
        #multiplerecognition(name)
        pass

def fetchfile(path):
    """This take a path to a directory that you want to referense, it will make a global variable such that one can use the function 'multiplerecognition'. """
    global correlationlist
    filepath = path
    correlationlist = []
    for file in os.listdir(filepath):
        if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
            currentfile  = os.path.join(filepath, file)
            correlationlist.append(currentfile)
    return correlationlist
    
def multiplerecognition(unknown):
    """This function will iterate through a libery of photos and return wheter it had a match in that liberary """
    correct = []
    for file in correlationlist:
        unknown1 = face_recognition.load_image_file(unknown)
        reference = face_recognition.load_image_file(file)
        unknown_encoding = face_recognition.face_encodings(unknown1)[0]
        referece_encoding = face_recognition.face_encodings(reference)[0]

        result = face_recognition.compare_faces([referece_encoding], unknown_encoding)
        print(f' The test for facial-recognition was {result}.')
        if result == [True]:
            correct.append(result)
    if len(correct)!=0:
        print('The person is in the correlation list')
    else:
        print('The person it not in the correlation list')
    
def recognition(unknown, reference):
    """ This takes an unknown image and compare it with an known image. If the face_recognition deems them to be the same person you will return true"""
    unknown = face_recognition.load_image_file(unknown)
    reference = face_recognition.load_image_file(reference)
    unknown_encoding = face_recognition.face_encodings(unknown)[0]
    referece_encoding = face_recognition.face_encodings(reference)[0]

    result = face_recognition.compare_faces([referece_encoding], unknown_encoding)
    print(f' The test for facial-recognition was {result}.')
    return result