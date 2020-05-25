import os, json, logging, sys
import thebe.core.data as data 

def setup(targetName):
    '''
    Checks if the command line argument file is ipynb format,
    if it is, write a new file of the same prefix to the same
    directory, containing only the source files in thebe format.
    Return that new file name and a true flag.

    If .py file extension, return the same file
    name that was inputted and a false flag.
    '''
    if isIpynb(targetName):
        ipynbFileContent = loadIpynb(targetName)
        tempName = write_temp(data.toThebe(ipynbFileContent), targetName)
        return tempName, True
    else:
        return targetName, False

        
def isIpynb(targetLocation):
    '''
    Return the target's file extension. 
    If input is incorrect, explain, and quit the application.
    '''
    if os.path.isfile(targetLocation):
        try:
            return test_extension(targetLocation) == 'ipynb'
        except ValueError:
            print('Please use a valid file extension. (.ipynb or .py)')
            sys.exit()
    else:
        print('Thebe only works with files, not directories. Please try again with a file. (.ipynb or .py)')
        sys.exit()

def test_extension(targetLocation):
    '''
    '''

    targetExtension=targetLocation.split('.')[-1]
    if targetExtension=='ipynb':
        return 'ipynb'
    elif targetExtension=='py':
        return 'py'
    else:
        print('Please use a valid file extension. (.ipynb or .py)')
        sys.exit()

def loadIpynb(fileName):
    '''
    Return the ipynb file as a dictionary.
    '''

    data = {}
    with open(fileName) as ipynb_data:
        data = json.load(ipynb_data)
    return data

def write_temp(initialData, fileName):
    '''
    Create a temporary file and load it with our initial data from the ipynb file.
    Open vim in our temporary file.
    '''
    filePrefix = getPrefix(fileName)
    tempFileName = '%s.py'%(filePrefix)

    try:
        with open(tempFileName, 'w') as f:
            f.write(initialData)
    except KeyboardInterrupt:
        removeTemp()

    return tempFileName

def removeTemp(tempFileName):
    '''
    '''
    os.remove(tempFileName)

def getPrefix(fileName):
    '''
    Get the file prefix
    '''

    # Doing this in a weird way to handle for situations where there are
    # dots other than the one signifying extension.
    splitName = fileName.split('.')
    splitName.pop()
    return '.'.join(splitName)


