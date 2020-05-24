import sqlite3

def check_table_exists(db,table):
    row= db.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name=?''', (table,)).fetchone()
    return (row is not None)

def dbsetup(db):
    if not check_table_exists(db,'meta'):
        db.execute('''CREATE TABLE meta (dbVersion INTEGER NOT NULL)''')
        db.execute('''INSERT INTO meta (dbVersion) VALUES (0)''')
        db.commit()
    (dbVersion,) = db.execute('''SELECT dbVersion FROM meta''').fetchone()

    if dbVersion == 0:
        db.execute('''CREATE TABLE data (key INTEGER PRIMARY KEY, value TEXT, expiry INTEGER NOT NULL)''')
        dbVersion = 1
        
    db.execute('''UPDATE meta SET dbVersion=?''', (dbVersion,))
    db.commit()
