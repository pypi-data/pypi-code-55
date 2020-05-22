from itertools import zip_longest
import time, sys, datetime, glob, re, sys, time, os, copy, logging
from hashlib import md5
from io import StringIO
from subprocess import Popen, PIPE
from flask import url_for
from pygments import highlight
from pygments.lexers import BashLexer, PythonLexer
from pygments.formatters import HtmlFormatter
from flask_socketio import emit, SocketIO
import thebe.core.constants as Constants
import thebe.core.logger as Logger

logger = Logger.getLogger('data.log', __name__)

def update(oldCellList, fileContent, runAll=False):
    '''
    Determine which cell has changed, since the file has changed.
    Return a list of cells, with updated sources, and the changed
    variable set.
    '''

    cellList = []
    sourceList = getSourceList(oldCellList)

    for cellCount, source in enumerate(fileContent.split(Constants.CellDelimiter)):

        #Split source by line
        source = source.splitlines(True)

        if validSource(source):
            # Get copy of cell initially populated
            cell = setChanged(oldCellList, sourceList, source)

            logger.info('Full source:\n\
                    ---------------\n\
                    %s'%(source,))

            # If outputs are empty, populate outputs
            # with an initial empty output so we 
            # don't get empty list errors
            if not cell['outputs']:
                cell['outputs'] = [Constants.getExecuteOutput()]

            # This activates if the user clicks the run all button
            if runAll:
                cell['changed']=True

            #Set execution counter if it exists
            try:
                cell['execution_count'] = oldCellList[cellCount]['execution_count'] 
            except IndexError:
                pass

            cellList.append(cell)

    return cellList

def getSourceList(cellList):
    '''
    Form the hashes from the cell list into a list
    '''
    return [cell['source'] for cell in cellList]

def toThebe(ipynb):
    '''
    Take in a ipynb dictionary, and returns a string in thebe format.
    (Cell sources to delimited by our Constants.CellDelimiter)
    '''

    output = ''
    for cell in ipynb['cells']:
        if cell['cell_type'] == 'markdown':
            output = ''. join(\
                    (output, \
                    (Constants.CellDelimiter + 'm\n' + \
                    ''.join(cell['source']))\
                    ))
        else:
            output = ''. join(\
                    (output, \
                    (Constants.CellDelimiter + '\n' + \
                    ''.join(cell['source']))\
                    ))
            logger.info('ipynb conversion output:\
                    \n-------------------------------\%s'%\
                    (output,))
    return output
    

def setChanged(oldCellList, sourceList, source):
    '''
    If the source preexists, set new cell to old cell
    If not, set changed, and last changed time.
    '''

    cell=copy.deepcopy(Constants.Cell)

    # Detect if cell is Markdown
    if source[0] == 'm\n':
        # Remove the markdown identifier
        source.pop(0)
        # Set cell as markdown
        cell['cell_type'] = 'markdown'
    else:
        # Remove the new line after the delimiter
        source.pop(0)

    #Set sourceCode
    cell['source'] = source

    try:
        x=sourceList.index(source)
        cell=oldCellList[x]

    except ValueError:
        cell['execution_count']
        cell['changed']=True
        cell['last_changed']=time.strftime("%x %X", time.gmtime())

    return cell

def hashSource(source):
    '''
    Hash the string of code
    '''
    return md5(source.encode()).hexdigest()

def validSource(source):
    '''
    Return false if source list is all Just new lines
    '''
    for s in source:
        if s != '\n':
            return True
    return False

