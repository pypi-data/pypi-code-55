import pytesseract
import urllib.request
import string
import os
import time
import re
import cv2
import webbrowser as web
import tkinter as tk
import numpy as np
import keyboard as key
from PIL import Image

width = 50
height = 0
newwidth = 0
arr = string.ascii_letters
arr = arr + string.digits + "+,.-? "


def feedback():
    """Contact developer"""
    print("For any querry, feedback, suggestions or contributions, contact me here 'ankitrajjitendra@gmail.com'")

def convert_text(string,rgb=[0,0,138]):
    """Convert the texts passed into handwritten characters"""
    global arr, width, height, back
    rgb.reverse()
    count = -1
    lst = string.split()
    for letter in string:
        if letter in arr:
            if letter == " ":
                count += 1
                letter = "zspace"
                wrdlen = len(lst[count+1])
                if wrdlen*110 >= back.width-width:
                    width = 0
                    height = height+227
                
            if letter.isupper():
                letter = "c"+letter.lower()
            if letter == ",":
                letter = "coma"
            if letter == ".":
                letter = "fs"
            if letter == "?":
                letter = "que"
            if width + 150 >= back.width:
                height = height + 227
                width = 50
            getimg(letter,rgb)
    back.show()
    back.close()
    back = Image.open(imgfolder+"\zback.png")
    width = 50
    height = 0
    newwidth = 0

def addTessPth(path):
    """Add path of tesseract binary distribution"""
    try:
        file = open("pydomyworkdata.py")
        data = file.read()
        imgfolder = re.search('tesspath : (.+)',data).group(1)
        file.close()
        cond = input("A path already added before, add anyway? (y/n): ")
        if cond == "y":
            with open("pydomyworkdata.py") as file:
                for lines in file:
                    if "imgpath" in lines:
                        cont = lines   
                file.close()
            with open("pydomyworkdata.py","w") as file:
                file.write(r"%stesspath : %s"%(cont,path))
                file.close()
            print("Path added successfully!")
            pytesseract.pytesseract.tesseract_cmd = path
    except:
        file = open("pydomyworkdata.py","a")
        file.write("tesspath : %s"%path)
        file.close()
        print("Path added successfully!")
        pytesseract.pytesseract.tesseract_cmd = path

def getimg(case,col):
    global width,height,back
    file = open("pydomyworkdata.py")
    data = file.read()
    imgfolder = re.search('imgpath : (.+)',data).group(1)
    file.close()
    img = cv2.imread(imgfolder+"/%s.png"%case)
    img[np.where((img!=[255,255,255]).all(axis=2))] = col
    cv2.imwrite(imgfolder+"/chr.png",img)
    cases = Image.open(imgfolder+"/chr.png")
    back.paste(cases,(width,height))
    newwidth = cases.width
    width = width + newwidth

def download():
    """Downloads all images of handwritten characters,\nthey are written by the author of this library"""
    def down(char):
        url = "https://raw.githubusercontent.com/Ankit404butfound/HomeworkMachine/master/Image/%s"%char
        imglink=urllib.request.urlopen(url)
        imgNp=np.array(bytearray(imglink.read()))
        img = cv2.imdecode(imgNp,-1)
        cv2.imwrite(r"%s\%s"%(imgfolder,char),img)
        print(".",end="")
    try:
        getimg("zback")
        print("Images already downloaded!")
    except:
        print("Please wait! Downloading images...",end="")
        imgfolder = os.getcwd()+"\ChrImages"
        if not os.path.exists(imgfolder):
            os.makedirs(imgfolder)
            file = open("pydomyworkdata.py","a")
            file.write("imgpath : %s\n"%imgfolder)
            file.close()
        for letter in arr:
            if letter == " ":
                letter = "zspace"
            if letter.isupper():
                letter = "c"+letter.lower()
            if letter == ",":
                letter = "coma"
            if letter == ".":
                letter = "fs"
            if letter == "?":
                letter = "que"
            try:
                down(letter+".png")
            except:
                down(letter+".PNG")
        down("zback.png")
        print("\nDownload Complete!")

def img_to_handtxt(path, rgb=[0,0,138], print_imgtxt = True):
    """Convert content of image to handwritten texts"""
    try:
        content = pytesseract.image_to_string(path)
    except:
        raise ImageNotFoundException("Image not found")
    if print_imgtxt:
        print(content)
    convert_text(content,rgb)

try:
    file = open("pydomyworkdata.py")
except:
    file = open("pydomyworkdata.py","w")
    print("Namaste, from the creator of this library, Ankit Raj Mahapatra.")
    print("Call pydomywork.feedback() to contact me for any feedback, query or suggestions.")
    print("This message will not be shown again.")
    file.close()

file = open("pydomyworkdata.py")
data = file.read()
try:
    imgfolder = re.search('imgpath : (.+)',data).group(1)
    file.close()
    back = Image.open(imgfolder+"\zback.png")
except:
    print("Hnadwritten characters' images not found!")
    case = input("Would you like to download them? (y/n): ")
    if case.lower() == "y":
        download()
        file = open("pydomyworkdata.py")
        data = file.read()
        imgfolder = re.search('imgpath : (.+)',data).group(1)
        file.close()
        back = Image.open(imgfolder+"\zback.png")
    
try:
    file = open("pydomyworkdata.py")
    data = file.read()
    tesspath = re.search('tesspath : (.+)',data).group(1)
    pytesseract.pytesseract.tesseract_cmd = tesspath
    pytesseract.image_to_string(imgfolder+"\zspace.png")
except:
    print("Tesseract not found! Or path not valid\nConsider watching the tutorial to know what to do.")
    lnkcse = input("Would you like to watch the tutorial? (y/n): ")
    if lnkcse == "y":
        print("Opening YouTube")
        web.open("https://youtu.be/icMNZNdjTvc")
        print("As explained, after installing that tesseract file, \nyou need to call pydomywork.addTessPth(path) and add its path there.")
   


##from PIL import Image
##import cv2
##import numpy as np
####char = input()
####width = 0
####height = 0
####for let in char:
####    print(let)
####    back = Image.open("ChrImages/zback.png")
####    img = cv2.imread("ChrImages/%s.png"%let)
####    img[np.where((img!=[255,255,255]).all(axis=2))] = [255,10,10]
####    cv2.imwrite("C:/Users/pc/Desktop/Image/chr.png",img)
####    con = Image.open("C:/Users/pc/Desktop/Image/chr.png")
####    back.paste(con,(width,height))
####    newwidth = con.width
####    width = width+newwidth
####back.show()
##    
##from PIL import Image
##import string
##back = Image.open("ChrImages/zback.png")
##width,height = 50,0
##arr = string.ascii_lowercase
##arr = arr+" "
##
##def condn(case):
##    global width,height
##    print(case)
##    img = cv2.imread("ChrImages/%s.png"%case)
##    img[np.where((img!=[255,255,255]).all(axis=2))] = [0,0,255]
##    cv2.imwrite("C:/Users/pc/Desktop/chr.png",img)
##    cases = Image.open("C:/Users/pc/Desktop/chr.png")
##    back.paste(cases,(width,height))
##    newwidth = cases.width
##    width = width+newwidth
##
##inp = input()
##for letter in inp:
##    if letter in arr:
##        if letter == " ":
##            letter = "zzback"
##        condn(letter)
##back.show()
##
##
