from itertools import zip_longest
import time, sys, datetime, glob, re, sys, time, os, copy
from hashlib import md5
from io import StringIO
from subprocess import Popen, PIPE
from flask import url_for
from pygments import highlight
from pygments.lexers import BashLexer, PythonLexer
from pygments.formatters import HtmlFormatter
from flask_socketio import emit, SocketIO
import python_live.core.constants as Constant

def addSavePlot(fileString, myDir, plotCount):
    fileArrayWithPlot=[]
    savefigText="plt.savefig('"+myDir+"/static/plot"+str(plotCount)+".png')"
    match = re.compile(r"###p")
    items = re.findall(match, fileString)
    for item in items:
        savefigText="plt.savefig('"+myDir+"/static/plot"+str(plotCount)+".png')"
        fileString=fileString.replace(item, savefigText)
    return fileString 
def getPlotData(globalScope, localScope):
    code=Constant.GetPlot
    redirected_output=sys.stdout=StringIO()
    redirected_error=sys.stderr=StringIO()
    stdout=''
    stderr=''
    try:
        sys.path.append(os.getcwd())
        exec(code, globalScope, localScope)
        stdout=redirected_output.getvalue()
        stderr=''
    except Exception as e:
        stdout=redirected_output.getvalue()
        stderr=str(e)
    finally:
        sys.path.pop()
        sys.stdout=sys.__stdout__
        sys.stderr=sys.__stderr__
    if stdout==Constant.EmptyGraph:
        stdout=''
    return stdout
def updateChanged(cellsList):
    for cell in cellsList:
        cell['changed']=False
def updateLedgerPop(oldAllCells, fileString, ledger, myDir):
    allCellsList=[]
    newLedger=[]
    newCellsToRun=[]
    cellDelimiter='####\n'
    for cellCount, cell in enumerate(list(filter(None, fileString.split(cellDelimiter)))):
        cellHash=md5(cell.encode()).hexdigest()
        newLedger.append(cellHash)
        isChanged=False
        stdout=''
        stderr=''
        if cellHash not in ledger:
            isChanged=True
        for oldCell in oldAllCells:
#            print(oldCell['stdout'])
#            print(oldCell['hash'])
            if oldCell['hash']==cellHash:
                stdout=oldCell['stdout']
                stdtr=oldCell['stderr']
        allCellsList.append({'cellCount':str(cellCount), 'hash':cellHash, 'code':cell, 'plot':'', 'datetime': time.strftime("%x %X", time.gmtime()), 'changed': isChanged, 'stdout':stdout, 'stderr':stderr, 'image/png':''})
    newCellsToRun=getNewCellsToRun(ledger, allCellsList)
    return newLedger, allCellsList
def getNewCellsToRun(ledger, allCellsList):
    newCellsToRun=[]
    for currentCell, ledgerCell in zip_longest(allCellsList, ledger, fillvalue=None):
        if currentCell['hash']!=ledgerCell:
            currentCell['changed']=True
        newCellsToRun.append(currentCell)
    return newCellsToRun
def convertLedgerToHtml(cellList, part='all'):
    # Return a deep copy of cellList with code replaced with html-ized code
    tempCells=copy.deepcopy(cellList)
    for cell in tempCells:
        if part=='all':
            cell['code']=highlight(cell['code'], PythonLexer(), HtmlFormatter())
            if cell['image/png']:
                cell['image/png']='<img src="data:image/png;base64, '+cell['image/png']+'" />'
            if cell['stdout']:
                cell['stdout']=highlight(cell['stdout'], BashLexer(), HtmlFormatter())
            if cell['stderr']:
                cell['stderr']=highlight(cell['stderr'], BashLexer(), HtmlFormatter())
        if part=='output':
            if cell['image/png']:
                cell['image/png']='<img src="data:image/png;base64, '+cell['image/png']+'" />'
            if cell['stdout']:
                cell['stdout']=highlight(cell['stdout'], BashLexer(), HtmlFormatter())
            if cell['stderr']:
                cell['stderr']=highlight(cell['stderr'], BashLexer(), HtmlFormatter())

    return tempCells 
def runNewCells(cellsToRun, ledger, globalScope, localScope, myDir):
    cellOutput=[]
    for cellCount, cell in enumerate(cellsToRun):
        if cell['changed']==True:
            stdout, stderr, plotData=runWithExec(cell['code'], globalScope, localScope)
            # Keep the master list updated
            cellsToRun[cellCount]['stdout']=stdout
            cellsToRun[cellCount]['stderr']=stderr
            cellsToRun[cellCount]['image/png']=plotData
            cellOutput.append({'stdout':stdout, 'stderr':stderr, 'image/png':plotData})
        else:
            cellOutput.append('')
    return cellOutput
def runWithExec(cellCode, globalScope, localScope):
    redirected_output=sys.stdout=StringIO()
    redirected_error=sys.stderr=StringIO()
    stdout=''
    stderr=''
    try:
        sys.path.append(os.getcwd())
        exec(cellCode, globalScope, localScope)
        stdout=redirected_output.getvalue()
        stderr=''
    except Exception as e:
        stdout=redirected_output.getvalue()
        stderr=str(e)
    finally:
        sys.path.pop()
        sys.stdout=sys.__stdout__
        sys.stderr=sys.__stderr__
    plotData=getPlotData(globalScope, localScope)
    return stdout, stderr, plotData
