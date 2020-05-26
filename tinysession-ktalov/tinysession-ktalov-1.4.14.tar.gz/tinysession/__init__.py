#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Gestiona sesiones en el lado servidor y controlar
de forma automaticamente su tiempo de vida por inactividad.

Ejemplo

from tinysession import TSession

#---------FUNCIONES REQUERIDAS PARA INTEGRAR TINYSESION-----------

def tinySession(operation, key='', value='', destroyIfTimeout=1):

    DEFAULT_KEYS = {'token':None}
    SESSION_TIMEOUT = 10
    SESSION_TRIGGER = tinyTimedOutTrigger
    tns = TSession('tinyDB', request, DEFAULT_KEYS, SESSION_TIMEOUT, SESSION_TRIGGER)
    if operation == 'createSession':
        tns(key)
    elif operation == 'destroySession':
        tns.destroySession()
    elif operation == 'addKey':
        tns.addKey(key, value, False)
    elif operation == 'getKey':
        tns.getKey(key, False)
    elif operation == 'setKey':
        tns.setKey(key, value, False)
    elif operation == 'isTimedOut':
        tns.isTimedOut(destroyIfTimeout)
    else:
        raise ValueError("La operacion indicada no es valida")
    return tns.tnsresult

def tinyTimedOutTrigger(sessionKeys):
    utoken = sessionKeys['__sessionToken']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE useraccess SET userToken='-', userState=0, loginDate=%(loginDate)s WHERE userToken=%(userToken)s;",{'loginDate':ctimeToDateTime('%Y-%m-%d %H:%M:%S'),'userToken':utoken})
    mysql.connection.commit()

#---------EJEMPLO DE USO------------
def isTimedOut(destroyIfTimeout=1):
    result = tinySession('isTimedOut', '', '', destroyIfTimeout)
    return result

def checkMe():
    isOut = isTimedOut(1)
    curFetch = (False,)
    if not isOut['isTimedOut']:
        #--Your code goes here
        curFetch = ''#cur.fetchall()
    response = {'apiResponse':curFetch, 'isTimedOut':isOut}
    return jsonify(response)

def login():
    token = '1231jkajksjkad'
    tinySession('createSession', token)                #Inicializa una sesion. NO es necesario volver a
                                                       #utilizar esto de nuevo en otro lado.
    tinySession('setKey', 'mytoken', token)            #Modifica una clave,en este caso esta clave se
                                                       #inicializo junto a la sesion
    tinySession('addKey, 'userID', 123)                #Agrega una nueva clave a la sesion    
    userId = tinySession('getKey', 'userID')['userID'] #Obtiene una clave de la sesion

"""

version     = "1.4.14"
__author__  = "Jose Ernesto Morales Ventura <jomorales.ventura@gmail.com>"
__credits__ = "Markus Siemens <markus@m-siemens.de> | tinylib author"

from tinydb import TinyDB, Query
import pathlib
import os
import datetime,time


class TSession(object):
    """
    Manejador de sesiones
    """


    def __init__(self, dbName, request, sessionKeys, sessionTimeOut, sessionTrigger):
        """
        Establece los parametros para crear una sesion. Los parametros se asignan
        cuando ejecute la operacion createSession.
        """

        self.sessionTrigger = sessionTrigger
        self.dbName = dbName
        if not '.json' in self.dbName.lower():
            self.dbName += '.json'

        self.request = request
        self.tableName = '%s~%s'%( self.__getRemoteAddr(request), str(request.user_agent).replace(' ', '').replace('/', '_') )

        #--Normaliza las claves de sesion
        if isinstance(sessionKeys, dict):
            self.sessionKeys = sessionKeys
        else:
            self.tnsresult = 'sessionKeys debe ser un diccionario de claves y valores que conforman la sesion'
            raise TypeError('sessionKeys debe ser un diccionario de claves y valores que conforman la sesion')
        
        #-- Normaliza el sessionTimeOut
        if isinstance(sessionTimeOut, float) or isinstance(sessionTimeOut, int) or isinstance(sessionTimeOut, str):
            try:
                self.sessionTimeOut = float(sessionTimeOut)
            except:
                self.tnsresult = 'sessionTimeOut debe ser numerico. Cada unidad es 1 segundo.'
                raise TypeError('sessionTimeOut debe ser numerico. Cada unidad es 1 segundo.')
            self.sessionTimeOut = sessionTimeOut
            self.sessionControl = {'sessionTimeOut':self.sessionTimeOut, 'lastAccess':time.time()}
        else:
            self.tnsresult = 'sessionTimeOut debe ser numerico. Cada unidad es 1 segundo.'
            raise TypeError(str(type(sessionTimeOut))+' sessionTimeOut debe ser numerico. Cada unidad es 1 segundo.')
        
    def __call__(self, sessionToken):
        """
        Crea una nueva sesion. Solo se crea si al verificar no existe, de lo contrario 
        este comando no tendra efecto y la sesion(tabla) existente se mantiene como estaba.
        """

        self.sessionToken = sessionToken
        self.__createFolder('tinysessions', 0o777)
        dataBase = self.__setDB()
        userTable = self.__setTable(dataBase)
        resp = self.__initializateTable(userTable, sessionToken)
        self.__createSessionControl(userTable, sessionToken)
        self.tnsresult = resp

    def __executeTrigger(self, keys):
        """
        Ordena la ejecucion del trigger que indico la API que se ejecute siempre que el periodo
        de inactividad se cumpla. Le devolvera a la API todas las claves de la sesion para que el
        mismo haga lo que necesite con ellas.
        """
        
        self.sessionTrigger(keys)
        
    def __getRemoteAddr(self, request):
        """
        Obtiene la direccion IP del host. 
        Esta IP se utiliza como nombre de la tabla que se crea para la sesion del usuario.
        """
        
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            return request.environ['REMOTE_ADDR']
        else:
            return request.environ['HTTP_X_FORWARDED_FOR']

    def __createFolder(self, folderName, mode):
        """
        Crea la carpeta contenedora de la(s) base(s) de dato(s)
        """
        
        fdir = pathlib.Path(folderName)
        
        if not os.path.exists(fdir):
            os.mkdir(folderName, mode)
            
        if os.path.exists(fdir):
            return True
        else:
            return False

    def __setDB(self):
        """
        Retorna una base de datos en la ruta indicada
        """
        
        return TinyDB(r'tinysessions/%s'%(self.dbName))

    def __openDatabase(self):
        """
        Abre y retorna la base de datos
        """

        database = None
        try:
            database = TinyDB(r'tinysessions/%s'%(self.dbName))
        except FileNotFoundError:
            raise FileNotFoundError('Aun no se ha creado algun controlador para la sesion')
        
        return database

    def __setTable(self, db):
        """
        Crea la tabla en la base de datos
        """
        
        return db.table(self.tableName)

    def __getTables(self):
        """
        Retorna las tablas existentes en una base de datos
        """
        
        dataBase = self.__openDatabase()
        return dataBase.tables()

    def __tableExists(self, tableName):
        """
        Valida si existe una tabla determinada en la base de datos
        """

        if tableName in self.__getTables():
            return True
        else:
            return False

    def __createSessionControl(self, table, sessionToken):
        """
        Crea variables para controlar el tiempo de actividad de la sesion
        """

        self.addKey('__sessionMaxTimeOut', self.sessionTimeOut, True)
        self.addKey('__sessionLastAccess', time.time(), True)
        self.addKey('__sessionToken', sessionToken, True)

    def __initializateTable(self, table, sessionToken):
        """
        Inserta una fila con las variables para controlar el TIMEOUT de la session.
        Inserta una fila con los campos que debe tener la sesion y sus valores por defecto.
        Solo se inicializa si la sesion NO esta activa.
        """

        if not self.__tableExists(self.tableName):
            if table.insert_multiple([self.sessionKeys]):
                self.tnsresult = {'status':True, 'response':'Ha sido creada una nueva sesion y se han insertado los datos correctamente'}
            else:
                self.tnsresult = {'status':False, 'response':'No fue posible inicializar la session'}
        else:
            self.tnsresult = {'status':False, 'response':'Existe una sesion activa'}
        
        return self.tnsresult

    def __toFile(self, fname, data):
        """
        Permite exportar informacion a un archivo de texto
        """

        fx = open(fname,'w')
        fx.write(str(data)+'\n')
        fx.close()
    
    def createSession(self, sessionToken):
        """
        Crea una nueva sesion. Solo se crea si al verificar no existe, de lo contrario 
        este comando no tendra efecto y la sesion(tabla) existente se mantiene como estaba.
        """

        self.sessionToken = sessionToken
        self.__createFolder('tinysessions', 0o777)
        dataBase = self.__setDB()
        userTable = self.__setTable(dataBase)
        resp = self.__initializateTable(userTable, sessionToken)
        self.__createSessionControl(userTable, sessionToken)
        self.tnsresult = resp

    def destroySession(self):
        """
        Destruye una session
        """

        dataBase = self.__openDatabase()
        dataBase.drop_table(self.tableName)
        if not self.__tableExists(self.tableName):
            self.tnsresult = {'status':True, 'response':'La session fue cerrada satisfactoriamente'}
        else:
            self.tnsresult = {'status':False, 'response':'No fue posible cerrar la sesion'}
        dataBase.close()
    
    def isTimedOut(self, destroyIfTimeout):
        """
        Calcula el tiempo de inactividad de una sesion y actualiza la clave __sessionlastaccess.
        destroyIfTimeout : Si la sesion esta sobrepasada en tiempo de inavtividad, la sesion sera destruida.
                 En otro caso solo devolvera el estado de la session
        """

        if self.__tableExists(self.tableName):
            nw = time.localtime(time.time())
            la = time.localtime(self.getKey('__sessionLastAccess',True)['__sessionLastAccess'])
            
            now = datetime.datetime(nw.tm_year, nw.tm_mon, nw.tm_mday, nw.tm_hour, nw.tm_min, nw.tm_sec)
            lastAccess = datetime.datetime(la.tm_year, la.tm_mon, la.tm_mday, la.tm_hour, la.tm_min, la.tm_sec)
            difference = abs((lastAccess - now).total_seconds())
            maxTime = abs(self.getKey('__sessionMaxTimeOut',True)['__sessionMaxTimeOut'])

            if difference >= maxTime:
                response = "Limite de tiempo excedido!."
                status = True
                if destroyIfTimeout:
                    #--Obtiene las claves antes de destruir la sesion
                    keys = self.getKey('*', True)
                    #-- Destruye la sesion
                    dataBase = self.__openDatabase()
                    dataBase.drop_table(self.tableName)
                    dataBase.close()
                    if not self.__tableExists(self.tableName):
                        self.__executeTrigger(keys)
                        response += "Esta session fue destruida satisfactoriamente"
                    else:
                        response += "No fue posible cerrar la sesion"
                else:
                    response += "La destruccion automatica de sesion no esta activada. -destroyIfTimeout=false-"
            else:
                response = "Sesion OK!"
                status = False

            self.setKey('__sessionLastAccess', time.time(), True)
            self.tnsresult = {'sessionResponse':response, 'sessionSeconds':difference, 'isTimedOut':status}
        else:
            response = 'No tiene sesion activa'
            self.tnsresult = {'sessionResponse':response, 'sessionSeconds':-1, 'isTimedOut':True}
        
        return self.tnsresult

    def addKey(self, key, value, privateMethod):
        """
        Agrega un campo a la sesion.Existen 3 tipos de variables de sesion.
        Method le indica a la funcion si quien llamo fue la API o si es una llamada interna.
        False es de la API, True es una peticion interna en la libreria
        """

        if privateMethod == False:
            #Verifica primero si no esta vencido el plazo de inactividad
            self.isTimedOut(True)
            
        if self.__tableExists(self.tableName):
            dataBase = self.__openDatabase()
            table = dataBase.table(self.tableName)
            try:
                value = float(value)
            except:
                value = value
            table.update({str(key):value}, doc_ids=[1])
            resp = self.getKey(str(key), True)

            return resp
        else:
            self.tnsresult = {'response':'No es posible agregar una clave, no hay una sesion activa', key:None, 'value':None}
            return self.tnsresult
    
    def getKey(self, key, privateMethod):
        """
        Obtiene un valor de la session del usuario.Utilice * para devolver todos los campos de sesion.
        Method le indica a la funcion si quien llamo fue la API o si es una llamada interna.
        False es de la API, True es una peticion interna en la libreria
        """

        if privateMethod == False:
            #Verifica primero si no esta vencido el plazo de inactividad
            self.isTimedOut(True)
            
        if self.__tableExists(self.tableName):
            #Client = Query()
            dataBase = self.__openDatabase()
            table = dataBase.table(self.tableName)
            if key == '*':
                allData = table.all()
                if allData.__len__() > 0:
                    #-- Retorna todas las claves
                    self.tnsresult = allData[0]
                else:
                    self.tnsresult = {None:None}
            else:
                try:
                    value = table.all()[0][str(key)]
                except:
                    value = None
                self.tnsresult = {key:value}
            dataBase.close()
        else:
            self.tnsresult = {'response':'No es posible obtener una clave, no hay una sesion activa', key:None}
        
        return self.tnsresult

    def setKey(self, key, value, privateMethod):
        """
        Asigna un valor a un campo en la session del usuario. 
        Retorna el valor presente antes de la modificacion y el valor
        luego de la modificacion.
        Method le indica a la funcion si quien llamo fue la API o si es una llamada interna.
        False es de la API, True es una peticion interna en la libreria
        """

        if privateMethod == False:
            #Verifica primero si no esta vencido el plazo de inactividad
            self.isTimedOut(True) 
            
        if self.__tableExists(self.tableName):
            if privateMethod == False:
                if str(key).lower() in ['__sessionToken', '__sessionlastaccess', '__sessionmaxtimeOut']:
                    raise KeyError("La clave %s es de dominio privado. No puedes modificar esta clave."%key)

            dataBase = self.__openDatabase()
            table = dataBase.table(self.tableName)

            #--Guarda el valor actual
            lastVal = table.all()
            if lastVal != []:
                lastVal = lastVal[0][str(key)]
            else:
                raise KeyError("La clave no %s existe"%str(key))

            #-- Modifica el valor
            try:
                value = float(value)
            except:
                None
            table.update({str(key):value})

            self.tnsresult = {'response':'setKey', 'lastValue':lastVal, 'newValue':table.all()[0][key]}
            dataBase.close()
        else:
            self.tnsresult = {'response':'No hay una sesion activa', 'lastValue':None, 'newValue':None}

        return self.tnsresult
