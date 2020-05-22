import sqlite3, logging, dill, os, sys, time
import thebe.core.constants as Constant
import thebe.core.logger as Logger
from datetime import datetime

logger = Logger.getLogger('database.log', __name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        if col[0] == 'cells' or col[0] == 'local_scope' or col[0] == 'global_scope':
            d[col[0]] = dill.loads(row[idx])
        else:
            d[col[0]] = row[idx]
    return d

DATABASE = '%s/database.sqlite' % os.path.dirname(os.path.abspath(__file__))

def getLedger(target):
    '''
    Get the data objects, if they do not exist create them.
    '''
    conn = sqlite3.connect(DATABASE, check_same_thread = False)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute('SELECT * FROM ledger WHERE name=?', (target,))
    fetched=c.fetchone()
    conn.close()
    if bool(fetched):
        r=fetched
        logger.info('Fetched Cells:\n-------------------------------\n%s'%(r['cells'],))
        return r['cells'], r['global_scope'], r['local_scope']
    else:
        createLedger(target)
        time.sleep(.5)
        return getLedger(target)

def createLedger(target):
    '''
    '''
    conn = sqlite3.connect(DATABASE, check_same_thread = False)
    conn.row_factory = dict_factory
    c = conn.cursor()
    logger.info('Adding\t%s\t to db...' % target)
    now=datetime.now().strftime('%a, %B, %d, %y')
    c.execute('INSERT INTO ledger (name, last_edit, created, cells, global_scope, local_scope, is_active) \
            VALUES (?,?,?,?,?,?,?)', (target, now, now, dill.dumps([]), dill.dumps({}), dill.dumps({}), False))
    conn.commit()
    conn.close()

def getExecutions(target):
    '''
    '''
    conn = sqlite3.connect(DATABASE, check_same_thread = False)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute('SELECT executions FROM ledger WHERE name=?', (target,))
    executions = c.fetchone()['executions']
    conn.close()
    return executions

def getIsActive(target):
    '''
    '''
    conn = sqlite3.connect(DATABASE, check_same_thread = False)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute('SELECT is_active FROM ledger WHERE name=?', (target,))
    isActive = c.fetchone()['is_active']
    conn.close()
    return isActive

def setIsActive(target):
    '''
    '''
    conn = sqlite3.connect(DATABASE, check_same_thread = False)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute('UPDATE ledger SET is_active=? WHERE name=?', \
            (True, target))
    conn.commit()
    conn.close()

def setActive(target, active):
    conn = sqlite3.connect(DATABASE, check_same_thread = False)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute('UPDATE ledger SET is_active=? WHERE name=?', (active, target))
    conn.commit()
    conn.close()

def update(target, cells, globalScope, localScope, executions):
    '''
    '''
    conn = sqlite3.connect(DATABASE, check_same_thread = False)
    conn.row_factory = dict_factory
    c = conn.cursor()
    localdump = {}
    try:
        localdump = dill.dumps(localScope)
    except AttributeError:
        logger.debug('Dill pickling the local scope, yields an error')
    logger.info('Before updating ledger with new cells:\n-------------------------------\n%s'%(cells,))
    c.execute('UPDATE ledger SET cells=?, global_scope=?, local_scope=?, executions=? WHERE name=?', \
            (dill.dumps(cells), dill.dumps(globalScope), dill.dumps(localdump), executions, target))
    conn.commit()
    conn.close()
