from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import cv2
import time
import imutils
import sys
import os
import re
import pickle

import numpy as np
from io import BytesIO

import os.path
import pkg_resources

import IPython.display
import PIL.Image
import tflite_runtime.interpreter as tflite

class Sandwich_Camera():
    def __init__(self):
        print("camera module ready")
        self.streamFlag = False
        
    def cameraInit(self):
        self.cam = cv2.VideoCapture(0)
        
        if( cam.isOpened() == False ):
            print("Unable to read camera feed")
            return
        
        self.cam.set(3,640)
        self.cam.set(4,480)
       
        self.flipFlag = True
        
        print("camera stream ready")
        
    def array_to_image(self, a, fmt='jpeg'):
        f = BytesIO()
        PIL.Image.fromarray(a).save(f, fmt)
    
        return IPython.display.Image(data=f.getvalue())
    
    def get_frame(self):
        ret, frame = self.cam.read()
        
        if( self.flipFlag == True ):
            frame = cv2.flip(frame, 1)
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        return frame
    
    def set_flipflag(self, flag):
        self.flipFlag = flag
        
    def cameraStream(self):
        if( self.streamFlag == True ):
            print("The camera is already working.")
            return
        
        d = IPython.display.display("", display_id=1)
        d2 = IPython.display.display("", display_id=2)
        while self.streamFlag:
            t1 = time.time()
            frame = self.get_frame()
            im = self.array_to_image(frame)
            d.update(im)
            t2 = time.time()
            s = f"""{int(1/(t2-t1))} FPS"""
            d2.update( IPython.display.HTML(s) )
            
    def cameraOff(self):
        if( self.streamFlag == False ):
            print("The camera is already stopped.")
            return
            
        self.cam.release()
        IPython.display.clear_output()
        print ("Stream stopped")
        
    def tensorflowInit(self):
        res_dir = pkg_resources.resource_filename(__package__,"res")
        
        model_file = res_dir + "/tensorflow/detect.tflite"
        label_file = res_dir + "/tensorflow/labelmap.txt"
        self.min_threshold = 0.5

        self.labels = self.load_labels(label_file)
        self.interpreter = tflite.Interpreter(model_path=model_file)
        self.interpreter.allocate_tensors()
        _, self.input_height, self.input_width, _ = self.interpreter.get_input_details()[0]['shape']
        
        print("Tensorflow ready")
    
    def load_labels(self, path):
        labels = {}
        
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
      
            for row_number, content in enumerate(lines):
                pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
                if( len(pair) == 2 and pair[0].strip().isdigit()):
                    labels[int(pair[0])] = pair[1].strip()
                else:
                    labels[row_number] = pair[0].strip()
        return labels
        
    def set_input_tensor(self, interpreter, input_image):
        tensor_index = interpreter.get_input_details()[0]['index']
        input_tensor = interpreter.tensor(tensor_index)()[0]
        input_tensor[:,:] = np.uint8(input_image)

    def get_output_tensor(self, interpreter, index):
        output_details = interpreter.get_output_details()[index]
        tensor = np.squeeze(interpreter.get_tensor(output_details['index']))

        return tensor

    def detect_object(self, interpreter, detect_image, threshold):
        self.set_input_tensor(interpreter, detect_image)
        interpreter.invoke()

        boxes = self.get_output_tensor(interpreter, 0)
        classes = self.get_output_tensor(interpreter, 1)
        scores = self.get_output_tensor(interpreter, 2)
        count = int(self.get_output_tensor(interpreter, 3))

        results = []
        for i in range(count):
            if scores[i] >= threshold:
                result = {
                  'bounding_box':boxes[i],
                  'class_id':classes[i],
                  'score':scores[i]
                }
                results.append(result)
    
        return results
        
    def tensorflowStream(self):
        if( self.streamFlag == True ):
            print("The camera is already working.")
            return
        
        d = IPython.display.display("", display_id=1)
        d2 = IPython.display.display("", display_id=2)
        while self.streamFlag:
            t1 = time.time()
            frame = self.get_frame()
            image_resized = cv2.resize(frame, (self.input_width,self.input_height))
            
            input_data = np.expand_dims(image_resized, axis=0)
            
            results = self.detect_object(self.interpreter, input_data, 0.5)
            
            for i in range(len(results)):
                if( (results[i]['score'] > self.min_threshold) and ( results[i]['score'] <= 1.0) ):
                    # draw rect
                    ymin, xmin, ymax, xmax = results[i]['bounding_box']
                    xmin = int(xmin * 640)
                    xmax = int(xmax * 640)
                    ymin = int(ymin * 480)
                    ymax = int(ymax * 480)

                    cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10,255, 0), 2)

                    # draw label
                    label = '%s: %d%%' % (self.labels[results[i]['class_id'] ], int(results[i]['score']*100))
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                    label_ymin = max(ymin, labelSize[1] + 10)
        
                    cv2.putText(frame, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2, cv2.LINE_AA)
            
            im = self.array_to_image(frame)
            d.update(im)
            t2 = time.time()
            s = f"""{int(1/(t2-t1))} FPS"""
            d2.update( IPython.display.HTML(s) )
            
    def tensorflowOff(self):
        if( self.streamFlag == False ):
            print("The camera is already stopped.")
            return
            
        self.cam.release()
        IPython.display.clear_output()
        print ("Tensorflow stopped")
        
    def facedetectorInit(self):
        res_dir = pkg_resources.resource_filename(__package__,"res")
        self.face_detector = res_dir + "/lbph/haarcascade_frontalface_alt.xml"
        self.face_datapath = res_dir + "/lbph/"
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        self.detect_flag = False
        self.savedata_flag = False
        self.saveface_name = "None"
        self.during_recognite = False
        
        with open(self.face_datapath + 'data.pickle', 'rb') as dataFile:
            self.recoDatas = pickle.load(dataFile)
        
        print("Facedetector ready")
    
    def trainModel(self):
        faces, ids = self.getFaceData(self.face_datapath + 'faces')
        self.recognizer.train(faces, np.array(ids))

        if not os.path.isdir(self.face_datapath + 'trainer'):
            os.makedirs(self.face_datapath + 'trainer')
        self.recognizer.save(self.face_datapath + 'trainer/trainer.yml')
        
    def facedetectorStream(self):
        if( self.streamFlag == True ):
            print("The camera is already working.")
            return
            
        d = IPython.display.display("", display_id=1)
        d2 = IPython.display.display("", display_id=2)
        while self.streamFlag:
            if self.during_recognite == True:
                continue
        
            t1 = time.time()
            frame = self.get_frame()
            im = self.array_to_image(frame)
            
            d.update(im)
            t2 = time.time()
            s = f"""{int(1/(t2-t1))} FPS"""
            d2.update( IPython.display.HTML(s) )
          
    def recognition(self, image):
        self.during_recognite = True
        name = "Unknown"
        x = 0
        y = 0
        w = 0
        h = 0

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector.detectMultiScale(gray, 1.2, 5, minSize=(40,40))

        for( x, y, w, h ) in faces:
            Id, conf = self.recognizer.predict(gray[y:y+h, x:x+w])
            cv2.rectangle(image, (x,y), (w,h), (10,255, 0), 2)
                           
            # draw label
            label = '%s: %d' % (self.recoDatas[Id], int(conf))
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            label_ymin = max(y, labelSize[1] + 10)
        
            cv2.putText(image, label, (x, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2, cv2.LINE_AA)
            
        self.during_recognite = False
        
    def faceRegistrationReady(self):
        if not os.path.isdir(self.face_datapath + 'faces'):
            os.makedirs(self.face_datapath + 'faces')
        self.initDataset()
        
    def faceRegistrationStart(self, name):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector.detectMultiScale(gray, 1.2, 5, minSize=(40,40))

        for( x, y, w, h ) in faces:
            face_image = gray[y:y+h, x:x+w]
            self.saveFaceData(face_image)
        
    def initDataset(self):
        datas = 0
        write = False

        if not os.path.exists(self.face_datapath + "data.pickle"):
            with open(self.face_datapath + 'data.pickle', 'wb') as dataFile:
                pickle.dump({}, dataFile, protocol=pickle.HIGHEST_PROTOCOL)

        with open(self.face_datapath + 'data.pickle', 'rb') as dataFile:
            datas = pickle.load(dataFile)
            names = list(datas.values())

            if not self.saveface_name in names and self.saveface_name is not None:
                number = len(datas)
                datas[number] = self.saveface_name
                write = True
        
        if write:
            with open(self.face_datapath + 'data.pickle', 'wb') as dataFile:
                pickle.dump(datas, dataFile, protocol=pickle.HIGHEST_PROTOCOL)
    
    def facedetectorOff(self):
        if( self.streamFlag == False ):
            print("The camera is already stopped.")
            return
            
        self.cam.release()
        IPython.display.clear_output()
        print ("Facedetect stopped")
        
        
        
        
        
        
