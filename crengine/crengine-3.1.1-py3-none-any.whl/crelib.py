######################################################################
### Change Ringing Engine
### Copyright (c) 2020 Jonathan Wilson
### Please refer to help/licence.txt for further information
### File: crelib.py
### Description: Support for sqlite3 database
### Last Modified: 24 May 2020
######################################################################

### import modules

import sqlite3
import os
import os.path
import csv
from . import ringing

######################################################################
### Class: CRELib
######################################################################

class CRELib():

    ### initialisation

    def __init__(self,dbase):
        self.dbase=dbase

    ### exists - check that database exists

    def exists(self):
        return os.path.isfile(self.dbase)

    ### drop - drop database

    def drop(self):
        if self.exists():
            os.remove(self.dbase)

    ### create - create database and table structure

    def create(self):
        for sql in sqls_dbase:
            self.runsql(sql,())

    ### initialise - initialise tables

    def initialise(self):

        # populate "stagename" table
        sql='insert into stagename values (?,?)'
        for n in ringing.stagenames.keys():
            args=(str(n),ringing.stagenames[n].title(),)
            self.runsql(sql,args)

        # populate methods with plain hunt
        sql='insert into method values (?,?,?,?,?,?)'
        for n in ringing.stagenames.keys():
            args=('Plain Hunt',str(n),ringing.plainhuntpn(n),0,'','',)
            self.runsql(sql,args)

    ### fetchmethod - return a single method

    def fetchmethod(self,mkey):
        return self.fetch(sql_fetchmethod,(mkey,))

    ### fetchnames - return a list of method names

    def fetchnames(self,mkey,nbells_min,nbells_max):
        qkey=mkey.replace('*','%').replace('?','_')
        args=(qkey,qkey,nbells_min,nbells_max,)
        results=self.fetch(sql_fetchnames,args)
        return [str(name) for row in results for name in row]

    ### fetchtowers - returns matching towers

    def fetchtowers(self,tkey):
        qkey=tkey.replace('*','%').replace('?','_')
        return self.fetch(sql_fetchtower,(qkey,))

    ### fetchbellmaps - returns bellmaps for a tower

    def fetchbellmaps(self,name):
        return self.fetch(sql_fetchbellmap,(name,))

    ### loadmethods - load methods

    def loadmethods(self,filename):
        return self.loadtable('method',['basename','nbells','plainlead','callrow','bob','single'],filename)

    ### loadtowers - load tower info

    def loadtowers(self,filename):
        return self.loadtable('tower',['name','description','samples','nbells','bellset'],filename)

    ### loadbellmaps - load bellmaps

    def loadbellmaps(self,filename):
        return self.loadtable('bellmap',['name','nbells','map'],filename)

    ### loadtable - load rows from CSV into a table

    def loadtable(self,table,cols,filename):

        # build query
        n=len(cols)
        sql='insert into %s (%s) values (%s)' %(
            table, ','.join(cols), ','.join(['?']*n))

        # open file
        with open(filename,'r') as fp:
            header=next(csv.reader(fp,delimiter=',',quotechar='"'))
            lines=list(csv.reader(fp,delimiter=',',quotechar='"'))

        # insert lines
        with sqlite3.connect(self.dbase) as cn:
            cr=cn.cursor()
            for line in lines:
                fields=line+['']*n
                args=tuple(fields[0:n])
                cr.execute(sql,args)
            cr.close()
            cn.commit()

        # return number of methods loaded
        return len(lines)

    ### fetch - fetch data into a list of rows

    def fetch(self,sql,args):
        with sqlite3.connect(self.dbase) as cn:
            cr=cn.cursor()
            cr.execute(sql,args)
            results=[list(row) for row in cr.fetchall()]
            cr.close()
        return results


    ### runsql - run query

    def runsql(self,sql,args):
        with sqlite3.connect(self.dbase) as cn:
            cr=cn.cursor()
            cr.execute(sql,args)
            cn.commit()
            cr.close()


######################################################################
### SQL Queries
######################################################################

### sqls_dbase - database structure

sqls_dbase=[
# method
'''create table method (
basename varchar(100)
, nbells int
, plainlead varchar(100)
, callrow int, bob varchar(100)
, single varchar(100)
, primary key (basename, nbells)
)'''
# stagename
, '''create table stagename (
nbells int primary key
, stagename varchar(25)
)'''
# tower
, '''create table tower (
name varchar(100) primary key
, description varchar(100)
, samples varchar(100)
, nbells int
, bellset varchar(100)
)'''
# bellmap
, '''create table bellmap (
name varchar(100)
, nbells int
, map varchar(100)
, primary key (name,nbells)
)'''
# method2
,'''create view method2 as
select m.basename||' '||n.stagename as fullname
, m.basename
, m.nbells
, m.plainlead
, m.callrow
, m.bob
, m.single
from method as m
inner join stagename as n
on n.nbells=m.nbells
''']

### sql_fetchmethod

sql_fetchmethod='''\
select basename,nbells,plainlead,callrow,bob,single
from method2
where fullname=?'''

### sql_fetchnames

sql_fetchnames='''\
select fullname from method2
where (fullname like ? or basename like ?)
and nbells between ? and ?
order by nbells, basename'''

### sql_fetchtower

sql_fetchtower='''\
select name, description, ifnull(samples,name) as samples, nbells, bellset
from tower
where name like ?'''

### sql_fetchbellmap

sql_fetchbellmap='''\
select name, nbells, map
from bellmap
where name=?'''


