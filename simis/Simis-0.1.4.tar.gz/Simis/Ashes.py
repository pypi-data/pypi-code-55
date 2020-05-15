from PySide2.QtCore import QObject, QIODevice, QDataStream, QByteArray, QCborValue, QCborMap, QDateTime
from PySide2.QtNetwork import QLocalSocket
import sys
import re
import time

# An exception class for the Ashes module
class AshesException(Exception):
    """Base class for other exceptions"""
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class AshesCouldNotConnectToServer(AshesException):
    """Raised when the socket cannot connect to the server"""
    def __init__(self, expression="", message=""):
        self.expression = expression
        self.message = message

class AshesLostConnectionToServer(AshesException):
    """Raised when the server stopped responding"""
    def __init__(self, expression="", message=""):
        self.expression = expression
        self.message = message

class AshesMissingCallbackFunction(AshesException):
    """Raised when callback function does not exist"""
    def __init__(self, expression="", message=""):
        self.expression = expression
        self.message = message

class AshesInvalidCallbackFunction(AshesException):
    """Raised when callback function either does not take the required arguments or does not return a model"""
    def __init__(self, expression="", message=""):
        self.expression = expression
        self.message = message

class Model(object):
    def __init__(self):
        pass

class Ashes(QObject):
    """This is a class for exchange between Ashes application and Python code"""
    def __init__(self, maxTimeout=30000, debugModeOn = False):
        QObject.__init__(self)
        
        self.debugModeOn = debugModeOn
        self.maxTimeout = maxTimeout

        # Create the model that is used to store data from Ashes later
        self.model = Model()

        # This socket will be connected to the Ashes local server
        self.socket = QLocalSocket()

    def __makeValidName(self, name):
        """
        Replaces everything that is not alphanumeric or underscore and returns the new string.
        Example: Node 1 -> Node1
        """
        return re.sub(r'[^\w]', '', name)

    def __buildModelRecursively(self, cborMap, model):
        """
        Builds an object-like model based on the given QCborMap.
        Calls itself recursively to create the deeper levels.
        Note: Makes given map keys valid by removing all non-alphanumeric characters.
        """
        for key in cborMap.keys():
            # Modify the key to make it a valid member name
            modified_key = self.__makeValidName(key.toString())

            if cborMap.value(key).isMap():
                # If the value connected to the current key is another QCborMap,
                # we have to create another Model() level and call this function again.
                # In addition to adding the member to the model with the modified key,
                # we also add a reference to the member child, so that the user can either
                # use the modified name: Model.Node1
                # or the original name: Model.child["Node 1"]

                model.__setattr__(modified_key, Model())

                if not hasattr(model, "child"):
                    model.__setattr__("child", {key.toString(): model.__getattribute__(modified_key)})
                else:
                    model.__getattribute__("child")[key.toString()] = model.__getattribute__(modified_key)

                self.__buildModelRecursively(cborMap.value(key).toMap(), model.__getattribute__(modified_key))
            else:
                # If the value connected to the current key is not another QCborMap,
                # we have an actual value here and we add it as a member without adding 
                # it to the child member list. This is because the two values could otherwise
                # be changed independently.
                model.__setattr__(modified_key, cborMap.value(key).toDouble())

    def __updateModelRecursively(self, cborMap, model):
        """
        Updates the given model based on the given QCborMap.
        Note: This function does not change the model's structure (i.e.
              what members the model has but only the member's values).
        """
        for key in cborMap.keys():
            # Modify the key to get a valid member name
            modified_key = self.__makeValidName(key.toString())

            if cborMap.value(key).isMap():
                self.__updateModelRecursively(cborMap.value(key).toMap(), model.__getattribute__("child")[key.toString()])
            else:
                model.__setattr__(modified_key, cborMap.value(key).toDouble())

    def __modelToDict(self, model):
        """
        Creates a dictionary from the given model. 
        This is the counterpart to the buildModelRecursively function.
        """
        dictionary = {}

        # Here we are looping over all members of the model but we are only considering those which
        # do hold actual values. We are using the child member list for looping over all levels of
        # the model.
        for key in model.__dict__.keys():
            if type(model.__getattribute__(key)) != type({}) and type(model.__getattribute__(key)) != type(Model()):
                dictionary[key] = model.__getattribute__(key)

            if key == "child":
                for k in model.child:
                    dictionary[k] = self.__modelToDict(model.child[k])

        return dictionary

    def connect(self, callbackFunction, serverName = ""):
        """
        Connects callbackFunction to an Ashes update command sent from
        the server with the given serverName. If serverName is empty,
        the first command line argument will be used. If that is also not
        given, "ASHES-SERVER" is used.
        The callback function receives a Model() class instance.
        """

        # Check if server name is empty and set it to first command line argument
        if serverName == "":
            if len(sys.argv >= 2):
                serverName = sys.argv[1]
            else:
                serverName = "ASHES-SERVER"

        # Set up the local socket
        self.socket.connectToServer(serverName, QIODevice.ReadWrite)

        # Check if the socket can connect - otherwise, raise an exception
        if not self.socket.waitForConnected(self.maxTimeout):
            raise AshesCouldNotConnectToServer(self.socket.error())
        
        if self.debugModeOn:
            print("Successfully connected to Ashes application.")

        # Read the data from the server
        headerSize = 8 + 8 + 8
        time = 0.0
        command = 0
        dataSize = 0
        data = QByteArray()

        stream = QDataStream(self.socket)

        while self.socket.bytesAvailable() < headerSize:
             # Wait for the server to write data
            if not self.socket.waitForReadyRead(self.maxTimeout):
                raise AshesLostConnectionToServer()
        
            if not self.socket.state() == QLocalSocket.ConnectedState:
                sys.exit()

        stream = QDataStream(self.socket)
        time = stream.readDouble()
        command = stream.readInt64()
        dataSize = stream.readInt64()

        while self.socket.bytesAvailable() < dataSize:
            # Wait for the server to write data
            if not self.socket.waitForReadyRead(self.maxTimeout):
                raise AshesLostConnectionToServer()
        
            if not self.socket.state() == QLocalSocket.ConnectedState:
                sys.exit()

        stream >> data

        if self.debugModeOn:
            print("{} >> {} ({}bytes)".format(QDateTime.currentDateTime().toString(), "Received update command", data.size()))

        # Make a QCborValue from the received data
        cborValue = QCborValue.fromCbor(data)

        # Make data to map
        cborMap = cborValue.toMap()

        # Build a model from the data
        self.model = Model()
        self.__buildModelRecursively(cborMap, self.model)

        # Check if there is a callback function defined
        # and update the model already for timestep 0.
        try:
            self.model = callbackFunction(self.model)
            
            if not type(self.model) == type(Model()):
                raise AshesInvalidCallbackFunction()
        except NameError:
            raise AshesMissingCallbackFunction()
        except TypeError:
            raise AshesInvalidCallbackFunction()

        # Convert model back to cbor
        dictionary = self.__modelToDict(self.model)
        cborMap = QCborMap.fromVariantMap(dictionary)

        # Tell the server that we are done here
        data = cborMap.toCborValue().toCbor()
        out = QDataStream(self.socket)
        out.writeDouble(time)
        out.writeInt64(1)
        out.writeInt64(data.size())
        out << data

        while self.socket.bytesToWrite() > 0:
            if not self.socket.waitForBytesWritten(self.maxTimeout):
                raise AshesLostConnectionToServer()

        if self.debugModeOn:
            print("{} << {} ({}bytes)".format(QDateTime.currentDateTime().toString(), "Sent success command", data.size()))

        # Now we are going in a loop for each time step
        while True:
            # First wait for the server to send an update command
            message = ""
            time = 0.0
            dataSize = 0
            data = QByteArray()
            
            stream = QDataStream(self.socket)

            while self.socket.bytesAvailable() < headerSize:
                # Wait for the server to write data
                if not self.socket.waitForReadyRead(self.maxTimeout):
                    raise AshesLostConnectionToServer()
            
                if not self.socket.state() == QLocalSocket.ConnectedState:
                    sys.exit()

            stream = QDataStream(self.socket)
            time = stream.readDouble()
            command = stream.readInt64()
            dataSize = stream.readInt64()

            while self.socket.bytesAvailable() < dataSize:
                # Wait for the server to write data
                if not self.socket.waitForReadyRead(self.maxTimeout):
                    raise AshesLostConnectionToServer()
            
                if not self.socket.state() == QLocalSocket.ConnectedState:
                    sys.exit()

            stream >> data

            if self.debugModeOn:
                print("{} >> {} ({}bytes)".format(QDateTime.currentDateTime().toString(), "Received update command", data.size()))

            # Check the message
            if command == 1:
                # Make a QCborValue from the received data
                cborValue = QCborValue.fromCbor(data)

                # Make data to map
                cborMap = cborValue.toMap()

                # Update our model
                self.__updateModelRecursively(cborMap, self.model)

                # Update the model with the callback function
                self.model = callbackFunction(self.model)

                # Convert model back to cbor
                dictionary = self.__modelToDict(self.model)
                cborMap = QCborMap.fromVariantMap(dictionary)

                 # Tell the server that we are done here and return
                 # the data
                data = cborMap.toCborValue().toCbor()
                out = QDataStream(self.socket)
                out.writeDouble(time)
                out.writeInt64(1)
                out.writeInt64(data.size())
                out << data

                while self.socket.bytesToWrite() > 0:
                    if not self.socket.waitForBytesWritten(self.maxTimeout):
                        raise AshesLostConnectionToServer()

                if self.debugModeOn:
                    print("{} << {} ({}bytes)".format(QDateTime.currentDateTime().toString(), "Sent update command", data.size()))



