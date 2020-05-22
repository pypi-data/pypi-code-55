from itertools import zip_longest
from multiprocessing import Process
import time, sys, datetime, glob, re, sys, time, os, copy, logging, threading, queue
from hashlib import md5
from io import StringIO
from subprocess import Popen, PIPE
from flask import url_for
from pygments import highlight
from pygments.lexers import BashLexer, PythonLexer
from pygments.formatters import HtmlFormatter
from flask_socketio import emit, SocketIO
import thebe.core.constants as Constant
import thebe.core.output as output 
import thebe.core.logger as Logger
import thebe.core.update as Update

logger = Logger.getLogger('run.log', __name__)

def runNewCells(socketio, cellsToRun, globalScope, localScope, jc):
    '''
    Run each changed cell, returning the output.
    '''

    # Append cells containing updated output to this
    newCells = []

    # Toggle to true when the users code produces an
    # error so code execution can stop
    hasError = False
    for cellCount, cell in enumerate(cellsToRun):

        # Run changed code if it is not markdown
        # and no prior cell has triggered an error
        if cell['changed'] and cell['cell_type'] != 'markdown' and not hasError:
            socketio.emit('message', 'Running cell #%s...'%(cellCount))
            socketio.emit('loading', cellCount)
            logger.info('Current working directory:\t%s'%(os.getcwd()))
            logger.info('\n------------------------\nRunning cell #%s\n-------------------------------\
                    \nWith code:\n%s'%(cellCount, cell['source']))
#            stdout, stderr, plotData = runWithExec(socketio, cell['source'], globalScope, localScope)

            # Execute the code from the cell, stream 
            # outputs using socketio, and return output
            stdout, stderr, plotData = jExecute(socketio, cell['source'], globalScope, localScope, jc)

            # Prevent subsequent execution of code
            # if in error was found
            if stderr:
                hasError = True

            # Remove old outputs from cell
            clearOutputs(cell)

            # Add output data to cell
            fillPlot(cell, plotData)
            fillStdOut(cell, stdout)
            fillErr(cell, stderr)

            # How does ipython do this?
            cell['changed']=False
            cell['execution_count'] = cell['execution_count'] + 1
            logger.info('exe co: %s'%(cell['execution_count'],))

        # Append run cell the new cell list
        newCells.append(cell)

    # Stop the front end loading
    socketio.emit('stop loading')

    return newCells

def jExecute(socketio, code, globalScope, localScope, jc):
    '''
    '''

    code = ''.join(code)

    # Execute the code
    msg_id = jc.execute(code)

    # Collect the response payload
    # reply = jc.get_shell_msg(msg_id)

    # Get the execution status
    # When the execution state is "idle" it is complete
    io_msg_content = jc.get_iopub_msg(timeout=1)['content']

    # We're going to catch this here before we start polling
    if 'execution_state' in io_msg_content and io_msg_content['execution_state'] == 'idle':
        logger.debug('No output!')

    # Initialize the temp variable
    temp = {}

    # Initialize outputs
    stdout = ''
    stderr = ''
    plotData = ''

    # Continue polling for execution to complete
    # which is indicated by having an execution state of "idle"
    while True:
        # Save the last message content. This will hold the solution.
        # The next one has the idle execution state indicating the execution
        # is complete, but not the stdout output
        temp = io_msg_content

        # Check the message for various possibilities
        if 'data' in temp: # Indicates completed operation
            if 'image/png' in temp['data']:
                plotData =  temp['data']['image/png']
                socketio.emit('plot output', getPlotOutput(plotData))
        if 'name' in temp and temp['name'] == "stdout": # indicates output
            stdout = '%s\n%s' % (stdout, temp['text'])
            logger.info('Standard output:\t%s'%(stdout,))
            socketio.emit('output', stdout.split('\n'))
        if 'traceback' in temp: # Indicates error
            stderr = '%s\n%s' % (stderr, temp['evalue'])

        # Poll the message
#        if 'execution_state' in io_msg_content and io_msg_content['execution_state'] == 'idle':
#            break
        try:
            logger.info('Retrieving message...')
            io_msg_content = jc.get_iopub_msg()['content']
            time.sleep(.1)
            if 'execution_state' in io_msg_content and io_msg_content['execution_state'] == 'idle':
                break
        except queue.Empty:
            break

    return stdout, stderr, plotData

def runWithExec(socketio, cellCode, globalScope, localScope):
    '''
    runs one cell of code and return plotdata and std out/err
    '''
    #Remove magics
    newCellCode = [cell for cell in cellCode if cell[0] != '%']

    #Append the current working directory to path(not sure if this is necessary)
    sys.path.append(os.getcwd())
    
    #Save the old output location
    oldstdout = sys.stdout

    #Redirect system output, and initialize system error
    stdout = sys.stdout=StringIO()
    stderr = ''
    plotData = ''

    #Set cutoff var for output
    isRunning = queue.Queue()
    isRunning.put(True)
    #Create a thread to stream the output to the client during runtime.
    t = threading.Thread(target = Update.streamOutput, \
            args = (socketio, stdout, isRunning))  
    t.daemon = True
    t.start()

    #Run code and capture output, if there is an error stop running, and capture it.
    try:
        exec(''.join(newCellCode), globalScope, localScope)
        sys.stdout = oldstdout
        stdout = stdout.getvalue() 
        sys.path.pop()
        plotData = getPlotData(globalScope, localScope)

    except Exception as e:
#        globalScope = oldGlobalScope
#        localScope = oldLocalScope
        stderr = str(e)
        sys.stdout = oldstdout
        stdout = stdout.getvalue() 
        sys.path.pop()

    #Turn off streamOutput
    isRunning.put(False)

    return stdout, stderr, plotData

def getPlotData(globalScope, localScope):
    '''
    '''

    code=Constant.GetPlot
    redirected_output=sys.stdout=StringIO()
    redirected_error=sys.stderr=StringIO()
    stdout=''
    stderr=''
    sys.path.append(os.getcwd())
    try:
        exec(code, globalScope, localScope)
        stdout=redirected_output.getvalue().rstrip()
        stderr=''
    except Exception as e:
        stdout=redirected_output.getvalue()
        stderr=str(e)
    sys.path.pop()
    sys.stdout=sys.__stdout__
    sys.stderr=sys.__stderr__
    if stdout==Constant.EmptyGraph:
        stdout=''
    return stdout

def clearOutputs(cell):
    '''
    Replace list of outputs with an empty one.
    '''
    cell['outputs'] = []

def fillPlot(cell, plot):
    '''
    If an image exists in the plot variable, create and return a plot cell.
    '''
    if plot:
        output = Constant.getDisplayOutput()
        output['data']['image/png'] = plot
        cell['outputs'].append(output)
    return cell

def getPlotOutput(plot):
    '''
    '''
    output = Constant.getDisplayOutput()
    output['data']['image/png'] = plot
    return output


def fillStdOut(cell, stdOut):
    '''
    If an output exists in the stdOut variable append new output to cell reference.
    '''
    if stdOut:
        output = Constant.getExecuteOutput()
        output['data']['text/plain'] = stdOut.splitlines(True)
        cell['outputs'].append(output)

def fillErr(cell, err):
    '''
    If an output exists in the err variable, create and return a err cell.
    '''
    if err:
        output = Constant.getErrorOutput()
        output['traceback'] = err.splitlines(True)
        cell['outputs'].append(output)

