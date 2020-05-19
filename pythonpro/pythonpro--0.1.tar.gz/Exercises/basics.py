def inverseName():
    """
    This program receive a name and lastname and return them upside down
    :return:
    """
    name = input('Digite su nombre y Apellido : ')
    nameList = name.split()
    nameList[0] = nameList[0][::-1]
    nameList[1] = nameList[1][::-1]
    name = ' '.join(nameList)
    print('Su Nombre y Apellido Al revés son:\n', name)


def generateTupleandList():
    """
    This program receive a sequence of comma-separated numbers from user and
    :return a list and a tuple with those numbers.
    """
    numbers = '1,2,3,4,5'
    numbersList = numbers.split(',')
    numbersTuple = tuple(numbersList)
    print('This is a List = ', numbersList, '\n', 'This is Tuple = ', numbersTuple)


def extensionoffile():
    """
    This function accept a filename from the user and print the extension of that.
    :return:
    """
    filename = 'abc.java'
    filenameTemp = filename.split('.')
    print('Your file extension is : ', repr(filenameTemp[-1]))


def firstandlastelementList():
    """
    This function return the first and last colors from a List
    :return: string
    """
    color_list = ["Red", "Green", "White", "Black"]
    print('El Primer color es el :', repr(color_list[0]), '\nEl Último color es el :', repr(color_list[-1]))


inverseName()
generateTupleandList()
extensionoffile()
firstandlastelementList()
