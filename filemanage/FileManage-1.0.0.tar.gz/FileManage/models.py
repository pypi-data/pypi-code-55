# coding:utf-8

'''
@author:    daben_chen

models.py Realize the operation of new folder, file torture, delete, etc.
'''

import os
import shutil
from shutil import copyfile

cur_file_name = ""


def newFolderpath(folder_path):
    """
    New folder function under specified path
    """
    is_Exist = os.path.exists(folder_path)
    if not is_Exist:
        os.mkdir(folder_path)
    else:
        print("Sorry! The current folder already exists, the folder path is:" + folder_path)

def newFile(new_file_path):
    """
    Create any file
    """
    cur_file = open(new_file_path, "w")
    cur_file.close()

def copyFileToFile(file_path, new_file_path):
    """
    Copy the file to the specified file path
    """
    copyfile(file_path, new_file_path)

def copyFileToFolder(file_path, new_folder_path):
    """
    Copy the file to the specified folder path
    """
    global cur_file_name
    if file_path.find("/") >=0:
        list_file_path = file_path.split("/")
        cur_file_name = list_file_path[len(list_file_path) - 1]
    else:
        list_file_path = file_path.split('\\')
        cur_file_name = list_file_path[len(list_file_path) - 1]
    if new_folder_path.find("/") >= 0:
        if new_folder_path.endswith('/'):
            new_copy_path = new_folder_path + cur_file_name
            copyfile(file_path, new_copy_path)
        else:
            new_copy_path = new_folder_path + '/' + cur_file_name
            copyfile(file_path, new_copy_path)
    else:
        if new_folder_path.endswith("\\"):
            new_copy_path = new_folder_path + cur_file_name
            copyfile(file_path, new_copy_path)
        else:
            new_copy_path = new_folder_path + '\\' + cur_file_name
            copyfile(file_path, new_copy_path)

def copyFolderToFolder(folder_path, new_folder_path):
    """
    Copy the folder to the specified folder path and include the files inside
    """
    if not os.path.exists(folder_path):
        print("folder_path not exist!")
    if not os.path.exists(folder_path):
        print("new_folder_path nit exist!")
    for root,dirs,files in os.walk(folder_path,True):
        for eachfile in files:
            shutil.copy(os.path.join(root,eachfile),new_folder_path)

def deleteEmptyFolder(folder_path):
    """
    Delete the specified empty folder
    """
    os.rmdir(folder_path)

def deleteFolder(folder_path):
    """
    Delete the folder containing the contents of the file
    """
    shutil.rmtree(folder_path, True)

def deleteFile(file_path):
    """
    Delete the specified file
    """
    is_Exist = os.path.exists(file_path)
    if not is_Exist:
        print("The current file path does not exist!")
    else:
        os.remove(file_path)