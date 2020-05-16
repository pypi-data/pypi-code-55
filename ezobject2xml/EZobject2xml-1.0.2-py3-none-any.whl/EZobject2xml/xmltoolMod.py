##    EZObject2XML - Easily save any object data into a xml file
##    Copyright (C) 2020 Alexandre CHAPELLE
##
##    Permission is hereby granted, free of charge, to any person obtaining a copy
##    of this software and associated documentation files (the "Software"), to deal
##    in the Software without restriction, including without limitation the rights
##    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
##    copies of the Software, and to permit persons to whom the Software is
##    furnished to do so, subject to the following conditions:
##
##    The above copyright notice and this permission notice shall be included in all
##    copies or substantial portions of the Software.
##
##    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
##    SOFTWARE.
##
##    More information by e-mail: alexandre.chapelle@yahoo.fr


""" The aim of this module is to easily save and load any object data into/from a xml file.

This module has only one object xmltool with 2 functions.
For saving an object into a xml file, you just have to write:
myxmltool = xmltool()
myxmltool.saveObject2xml(myObject,myFilename)
And for loading:
myxmltool.loadObjectFromXml(myObject,myFilename)
"""

##todo
##nothing for now

__version__ = '1.0.2' #last change in 05152020

class SingleType():
    """ This object is only used to transtype a single value data as integer, float, string, set, tuple, list or dict to an object.

    This is needed to use saveObject2xml function with a single value data.
    For saving any value as int, float, str, set, tuple, list or dict, you just have to code:
    $ myxmltool = xmltool()
    $ myvalue_object = SingleType(myvalue)
    $ myxmltool.saveObject2xml(myvalue_object,'myvalue.xml')

    For loading:
    $ myxmltool.loadObjectFromXml(myvalue_object,'myvalue.xml')
    $ myvalue = myvalue_object.value
    """
    
    def __init__(self,value = None):
        """
        Parameters
        ----------
        value: any basic data type as int, float, str, set, tuple, list or dict
        """
        
        self.value = value

class initDataList():
    """ This object contains a list of all information to create new instances of different objects with the given parameters.

    This is neeeded when we want to load an object containing itself an undefined number of object (in a list or set).
    We use these data to create a first instance of these objects and then load the xml data into this object
    To use this function, i.e.:
    $ myInitDataList.addInitData(myObjectClass,(a tuple containing my parameters to initialize this object))
    """
    
    def __init__(self):
        self.__list = list()
    def addInitData(self,objectClass, initParam: tuple = None):
        """ Add the information to create a new instance of a given object with the given parameters
        
        Parameters
        ----------
        objectClass: class
            Any object class that we could use to create a new instance of an object
        initParam:tuple, optional
            This tuple must contain all the parameters in the right order to initialize the new instance of the object (default = None)
        """

        self.__list.append((objectClass,initParam))
    def getInitData(self,objectClassName: str):
        """ get the information to create a new instance of a given object with the given parameters
        
        Parameters
        ----------
        objectClassName: str
            Any object class name that we use to find the information matching in the list to create a new instance of an object
        
        Returns
        -------
        the data to initialize an object or None if not found
        """
        for i in range(len(self.__list)):
            if self.__list[i][0].__name__ == objectClassName:
                return self.__list[i]
        return None

class xmltool():
    """This is basic object to access the functions"""
    
    def __init__(self):
        self.__filename = str()
        self.__theObject = object()
        self.__xmltool = None
        self.__file2beClosed = False
        self.__initDataList = list()
        self.__FOLLOWREADEDLINES = False #for debugging only, print all lines during processing
        
#---------------------------------------------------------------
#common functions

    def __openxmltool(self,mode:str) -> bool: #mode should be 'w' for writing or 'r' for reading
        if self.__xmltool == None:
            try:
                self.__xmltool = open(self.__filename,mode)
                self.__file2beClosed = True
                if mode == 'w':
                    self.__xmltool.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                if mode == 'r':
                    textline = self.__xmltool.readline()[0:5]
                    if self.__FOLLOWREADEDLINES:
                        print(textline)
                    if  textline != '<?xml':
                        print("EZobject2xml_1_0_2.xmltoolMod.xmltool.__openxmltool:")
                        print("The file " + self.__filename + " is not a xml File.")
                        print("The file should begin with a '<?xml' statement.")
                        print("(error_code: 0.0.1.132)")
                        return False
                return True
            except:
                print("EZobject2xml_1_0_2.xmltoolMod.xmltool.__openxmltool:")
                print("The file " + self.__filename + " cannot be accessed.")
                print("(error_code: 0.0.1.138)")
                return False
        return True

    def __closexmltool(self)-> bool:
        if self.__file2beClosed == True:
            self.__xmltool.close()
        self.__xmltool = None
        return True
            
#---------------------------------------------------------------
#save and write functions

    def saveObject2xml(self,object2save: object, filename: str, name: str = None)-> bool:
        """ Save any object data into a xml file

        Parameters
        ----------
        object2save: object
            Any object to save the data into a xml file
        filename: string
            The name of the xml file
        name: str, optional
            The name of the object to save (default is None)

        Returns
        -------
        True if all the method was well proceeded
        """
        
        self.__theObject = object2save
        self.__filename = filename
        if self.__openxmltool('w') == False:
            return False
        #call the optional save2XML function
        if hasattr(self.__theObject,'save2xml'):
            self.__theObject.save2xml(self.__xmltool,name)
            return True
        #self.__writeObject(self.__theObject,name)
        self.__writeVariable(self.__theObject,name)
        self.__closexmltool()
        return True
    
    def __writeSingleValue(self,value,varName = None):
        self.__xmltool.write("<value")
        if varName != None:
            self.__xmltool.write(" name='" + varName + "'")
        self.__xmltool.write(">")
        theType = type(value)
        if theType == str:
            self.__xmltool.write("'" + value + "'")
        else:
            self.__xmltool.write(str(value))
        self.__xmltool.write('</value>\n')

    def __writeMultiValue(self,value,varName = None):
        self.__xmltool.write("<multiValue type='")
        if type(value)== tuple:
            self.__xmltool.write("tuple'")
        if type(value)== set:
            self.__xmltool.write("set'")
        if type(value)== dict:
            self.__xmltool.write("dict'")
        if type(value)== list:
            self.__xmltool.write("list'")
        if varName != None:
            self.__xmltool.write(" name='" + varName + "'")
        self.__xmltool.write(">\n")
        if type(value)== list or type(value)== tuple:
            for i in range(len(value)):
                self.__writeVariable(value[i])
        if type(value)== set:
            for subValue in value:
                self.__writeVariable(subValue)
        if type(value) == dict:
            for keys in value:
                self.__xmltool.write("<value name='keys'>'"+str(keys)+"'</value>\n")
                self.__writeVariable(value[keys])
        self.__xmltool.write('</multiValue>\n')

    def __writeObject(self,object2write,name):
        self.__xmltool.write("<object")
        if name != None:
            self.__xmltool.write(" name='" + name + "'")    
        self.__xmltool.write(" class='" + object2write.__class__.__name__ + "'>\n")
        varNames = [attr for attr in dir(object2write) if not callable(getattr(object2write, attr)) and not attr.endswith("__")]
        for varName in varNames:
            self.__writeVariable(getattr(object2write,varName),varName)          
        self.__xmltool.write('</object>\n')

    def __writeVariable(self,variable,name = None):
        varType = type(variable)
        if varType == int or varType == float or varType == str or varType == bool or variable == None or varType == complex:
            self.__writeSingleValue(variable,name)
        elif varType == tuple or varType == set or varType == dict or varType == list:
            self.__writeMultiValue(variable,name)
        else:
            self.__writeObject(variable,name)

#---------------------------------------------------------------
#load and read functions

    def loadObjectFromXml(self,object2read:object, filename: str, theInitDataList:initDataList = None)-> bool: 
        """ Load data from a xml file to any object containing the same data structure

        Parameters
        ----------
        object2read: object
            Any object to load the data from a xml file
        filename: string
            The name of the xml file
        initList:list, optional
            This list is needed only if objects have to be dynamically initialized during the data reading process.
            i.e. if your object has a list of an undefined number of other objects, we have to create them first before reading their saved data

        Returns
        ------
        True if all the method was well proceeded
        """
         
        self.__theObject = object2read
        self.__filename = filename
        self.__initDataList = theInitDataList
        if self.__openxmltool('r') == False:
            return False
        if hasattr(self.__theObject,'loadFromXml'):
            self.__theObject.loadFromXml(self.__xmltool,initList)
            return True
        textline = self.__xmltool.readline()
        if self.__getNode(textline) != 'object':
            print("EZobject2xml_1_0_2.xmltoolMod.xmltool.loadObjectFromXml : xml file and object to read do not match (error_code: 0.0.1.244)")
        else:
            self.__readObject(self.__theObject,textline)
        self.__closexmltool()
        return True

    def __getNode(self,textline):
        startpos = textline.find('<') + 1
        endpos = textline.find('>')
        space = textline.find(' ')
        if space!= -1 and space < endpos:
            endpos = space
        return textline[startpos:endpos]
        
    def __getProperty(self,propertyName,textline):
        startPos = textline.find(" " + propertyName + "='")
        if startPos == -1:
            return None
        startPos = startPos + len(" " + propertyName + "='")
        endPos = startPos + textline[startPos:-1].find("'")
        return textline[startPos:endPos]            
            
    def __readSingleValue(self,textline):
        startPos = textline.find('>') + 1
        try:
            if textline[startPos] == "'":
                startPos = startPos + 1
                endPos = startPos + textline[startPos:-1].find("'")
                return textline[startPos:endPos] #string
            elif textline[startPos] == '(':
                return complex(textline[startPos:textline.find(')')+1]) #complex
            elif textline[startPos:startPos+4] == 'True': #boolean
                return True
            elif textline[startPos:startPos+5] == 'False': #boolean
                return False
            elif textline[startPos:startPos+4] == 'None': #None
                return None
            elif textline[startPos:-1].find('.') != -1:
                return float(textline[startPos:startPos + textline[startPos:-1].find('<')]) #float
            else:
                return int(textline[startPos:startPos + textline[startPos:-1].find('<')])#integer
        except:
            print("EZobject2xml_1_0_2.xmltoolMod.xmltool.__readSingleValue:")
            print("The textline " + textline + " doesn't refer to a readable value.")
            print("(error_code: 0.0.1.312)")
            return None

    def __readMultiValue(self,textline):
        theList = list()
        theDict = dict()
        theType = self.__getProperty('type',textline)
        EOF = False
        while EOF == False:
            textline = self.__xmltool.readline()
            if self.__FOLLOWREADEDLINES:
                print(textline)
            if textline == '' or textline == '</multiValue>\n':
                EOF = True
                break
            if theType == 'tuple' or theType == 'list' or theType == 'set':
                theList.append(self.__readVariable(textline))
            if theType == 'dict':
                key = self.__readVariable(textline)
                value_textline = self.__xmltool.readline()
                if self.__FOLLOWREADEDLINES:
                    print(value_textline)
                value = self.__readVariable(value_textline)
                theDict[key] = value
        if theType == 'tuple':
            return tuple(theList)
        if theType == 'list':
            return theList
        if theType == 'set':
            return set(theList)
        if theType == 'dict':
            return theDict

    def __createObject(self,textline):
        classString = self.__getProperty('class',textline)
        if self.__initDataList == None:
            print("EZobject2xml_1_0_2.xmltoolMod.xmltool.__createObject:")
            print("You must pass a initDataList to initiate the class " + theClass)
            print("(error_code: 0.0.1.350)")
            return None
        newObject = None
        initData = self.__initDataList.getInitData(classString)
        if initData != None and initData[1] is tuple:
            if len(initData[1]) > 9:
                print("EZobject2xml_1_0_2.xmltoolMod.xmltool.__createObject :")
                print("The numbers of parameters to initiate the class " + theClass + " is exceeding 9.")
                print("(error_code: 0.0.1.358)")
            if len(initData[1]) == 9: #maximum 9 parameters
                newObject = initData[0](initData[1][0],initData[1][1],initData[1][2],initData[1][3],initData[1][4],initData[1][5],initData[1][6],initData[1][7],initData[1][8])
            if len(initData[1]) == 8:
                newObject = initData[0](initData[1][0],initData[1][1],initData[1][2],initData[1][3],initData[1][4],initData[1][5],initData[1][6],initData[1][7])
            if len(initData[1]) == 7:
                newObject = initData[0](initData[1][0],initData[1][1],initData[1][2],initData[1][3],initData[1][4],initData[1][5],initData[1][6])
            if len(initData[1]) == 6:
                newObject = initData[0](initData[1][0],initData[1][1],initData[1][2],initData[1][3],initData[1][4],initData[1][5])
            if len(initData[1]) == 5:
                newObject = initData[0](initData[1][0],initData[1][1],initData[1][2],initData[1][3],initData[1][4])
            if len(initData[1]) == 4:
                newObject = initData[0](initData[1][0],initData[1][1],initData[1][2],initData[1][3])
            if len(initData[1]) == 3:
                newObject = initData[0](initData[1][0],initData[1][1],initData[1][2])
            if len(initData[1]) == 2:
                newObject = initData[0](initData[1][0],initData[1][1])
            if len(initData[1]) == 1:
                newObject = initData[0](initData[1][0])
        elif initData[1] != None:
            newObject = initData[0](initData[1])
        else:
            newObject = initData[0]()
        if newObject == None:
            print("EZobject2xml_1_0_2.xmltoolMod.xmltool.__createObject:")
            print("Unable to initiate the class " + theClass)
            print("(error_code: 0.0.1.384)")
        return newObject

    def __readObject(self,object2read,textline=None):
        if textline == None:
            textline = self.__xmltool.readline() #read the class line
        if self.__FOLLOWREADEDLINES:
            print(textline) 
        EOF = False
        varNames = [attr for attr in dir(object2read) if not callable(getattr(object2read, attr)) and not attr.endswith("__")]
        while not EOF:
            textline = self.__xmltool.readline()
            if self.__FOLLOWREADEDLINES:
                print(textline)
            varName = self.__getProperty('name',textline)
            if textline == '' or textline == "</object>\n":
                EOF = True
                break
            elif varName in varNames: 
                setattr(object2read,varName,self.__readVariable(textline,object2read))
        return object2read
    
    def __readVariable(self,textline,actualObject = None):
        node = self.__getNode(textline)
        if node == 'value':
            return self.__readSingleValue(textline)
        elif node == 'multiValue':
            return self.__readMultiValue(textline)
        elif node == 'object':
            varName = self.__getProperty('name',textline)
            if varName != None:
                object2read = getattr(self.__theObject, varName)
            else:
                object2read = self.__createObject(textline)
            return self.__readObject(object2read,textline)
