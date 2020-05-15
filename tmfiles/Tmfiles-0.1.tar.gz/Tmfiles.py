#-------------------------------------------------------------------------------
# Name:        Tmfiles
# Purpose:موديول لقراءة الملفات والكتابة فيها
#
# Author:      moham
#
# Created:     15-05-2020
# Copyright:   (c) moham 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
class Tmfiles :
    def OpenToRead(self,sFile):
        f = open(sFile, "r+")
        print(f.read())


    def Open_To_Overwrite (self,sFile,wFile):#مسح الملف ثم الكتابة عليه
        f = open(sFile, "w+")
        f.write(wFile)
        f.close()


    def Open_To_Appendwrite (self,sFile,wFile):#اضافة نص جديد للملف
        f = open(sFile, "a")
        f.write(wFile)
        f.close()


    def Read_Ch_No(self,sfile,Chno):# قراءة عدد من الحروف من بداية النص
        f = open(sfile, "r")
        print(f.read(Chno))

    def Read_Firstline(self,sfile):# قراءة سطر واحد من الملف
        f = open(sfile, "r")
        print(f.readline())

    def Read_F2lines(self,sfile):# قراءة اول سطرين من الملف
        f = open(sfile, "r")
        print(f.readline())
        print(f.readline())
    def Read_LineByline(self,sfile):# قراءة سطر واحد من الملف
        f = open(sfile, "r")
        for x in f:
            print(x)

    def RemovFile(self,sfile):#حذف ملف
        if os.path.exists("demofile.txt"):
            os.remove(sfile)
        else:
            print("The file does not exist")

    def FolderDelete(self,nFolder):#حذف فولدر بكل ما يحتوي
        os.rmdir(nFolder)
















def main():
    pass

if __name__ == '__main__':
    main()
