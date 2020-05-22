import thebe.core.database as Database
import thebe.core.run as Run
import thebe.core.file as File
import thebe.core.html as Html
import thebe.core.data as data
import thebe.core.constants as Constants 
import thebe.core.logger as Logger
import os, time, json, threading, queue, copy
logger = Logger.getLogger('update.log', __name__)

def checkUpdate(socketio, fileLocation, connected=False, \
        isIpynb=False, GlobalScope=None, LocalScope=None, Cells=None, runAll=False, jc=None):
    '''
    '''
    
    '''
    If code is currently being executed,
    stop checkUpdate. Send some feedback to client.
    '''
    Cells, iGlobalScope, iLocalScope  = Database.getLedger(fileLocation)
    isActive = Database.getIsActive(fileLocation)

    #If the run all event is triggered
    if runAll:
        logger.info('Run All Has Been Triggered!')
        if isActive:
            socketio.emit('flash')
        else:
            thread = update(socketio, fileLocation, GlobalScope, LocalScope, Cells, isIpynb, jc, runAll)
            time.sleep(.5)

    #If it's modified or if it's the first time it has run, update.
    elif isModified(fileLocation):
        if isActive:
            logger.info('flashing')
            socketio.emit('flash')
        else:
            thread = update(socketio, fileLocation, GlobalScope, LocalScope, Cells, isIpynb, jc)
            time.sleep(.5)

    elif connected==True:
        if not isActive:
            if not Cells:
                thread = update(socketio, fileLocation, GlobalScope, LocalScope, Cells, isIpynb, jc)
            else: 
                socketio.emit('show all', Html.convert(Cells))
        else:
            socketio.emit('show all', Html.convert(Cells))

    else:
        pass
    time.sleep(.5)

#Run code and send code and outputs to client
def update(socketio, fileLocation, GlobalScope, LocalScope, Cells, isIpynb, jc, runAll=False):
    isActive = Database.setIsActive(fileLocation)

    '''
    Get some variables from database
    '''

    '''
    Get target file
    '''
    fileContent=''
    with open(fileLocation, 'r') as file_content:
        fileContent=file_content.read()
    '''
    Look at the file to see if anything has changed
    in the data.
    Return an updated ipynb,
    with proper changed values.
    '''
    logger.info('Output before update\n-------------------------------\n%s'%([cell['outputs'] for cell in Cells],))
    Cells = data.update(Cells, fileContent, runAll)
    logger.info('Output after update\n-------------------------------\n%s'%([cell['outputs'] for cell in Cells],))
    socketio.emit('show all', Html.convert(Cells))

    '''
    Send a list of the cells that will run to the
    client so it can show what is loading.
    '''
    def runThread(Cells, GlobalScope, LocalScope):
        '''
        Run the newly changed cells and return their output.
        '''
        Cells = Run.runNewCells(socketio, Cells, GlobalScope, LocalScope, jc)
        executions = Database.getExecutions(fileLocation)
        executions += 1
        logger.info('The number of code executions is %d' % executions)
#        socketio.emit('show all', Html.convert(Cells))
        
        '''
        Update the database with the fresh code.
        And outputs.
        '''
        Database.setActive(fileLocation, False)
        Database.update(fileLocation, Cells, GlobalScope, LocalScope, executions)
        updateIpynb(fileLocation, Cells)
    t = threading.Thread(target = runThread, args = (Cells, GlobalScope, LocalScope))
    t.daemon = True
    t.start()
    return t

def updateIpynb(fileLocation, Cells):
    '''
    Write the new changes to the ipynb file.
    '''
    cCells = copy.deepcopy(Cells)

    # Remove extra attributes created by thebe.
    sanitize(cCells)
    

    # Save cells into a ".ipynb" file
    with open(File.getPrefix(fileLocation)+'.ipynb', 'w') as f:
        # Get the jupyter cell list wrapper
        ipynb = Constants.getIpynb()
        # Wrap cells
        ipynb['cells'] = cCells
        # Overwrite old ipynb file
        json.dump(ipynb, f, indent=True)

def sanitize(Cells):
    '''
    Remove the extra attributes that thebe uses,
    that Jupyter does not
    '''
    for i, cell in enumerate(Cells):
        del Cells[i]['execution_count']
        del Cells[i]['changed']

def isModified(fileLocation, x=.3):
    '''
    Return true if the target file has been modified in the past x amount of time
    '''

    lastModified=os.path.getmtime(fileLocation)
    timeSinceModified=int(time.time()-lastModified)

    if timeSinceModified<=x:
        return True
    else:
        return False

def streamOutput(socketio, stream, isRunning):
    '''
    Send new output to the client on the fly.

    Intended to run for the duration of one cell.
    Which is when the queue, isRunning, is false.
    '''
    oldStream = ''
    while list(isRunning.queue)[-1]:
        currentStream = stream.getvalue()
        if not currentStream == oldStream:
            socketio.emit('output', currentStream.split('\n'))
            oldStream = currentStream
        # Sleep the loop so it doesn't pollute the socket. The length is currently arbitrary.
        time.sleep(.2)


