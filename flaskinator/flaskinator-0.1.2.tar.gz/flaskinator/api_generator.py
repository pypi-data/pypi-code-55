import os

class FlaskApiGenerator:

    def __init__(self):
        self.__FLASK_HEADER = '''from flask import Flask,request
        import json
        app = Flask(__name__)'''

        self.__FLASK_FOOTER = '\n\n\napp.run()'

        self.__FLASK_API_GET_ROUTE_HEADER = '''\n\n@app.route("/%s")''' #replace %s with the route
        self.__FLASK_API_POST_ROUTE_HEADER = '''\n\n@app.route("/%s", methods=['POST'])''' #replace %s with the route
        self.__FLASK_DEF_DECLARATION = ''' \ndef %s(%s):''' #replace the function name and the function parameters
        self.__FLASK_DEF_BODY_WITH_RESPONSE = '''\n\t#Write logic here\n\treturn json.dumps(%s().__dict__)''' #%s to replace response class name
        self.__FLASK_DEF_BODY_WITHOUT_RESPONSE = '''\n\t#Write logic here\n\tpass'''

        #Path variables. Here %s replaces with the variable name.
        self.__FLASK_PATH_VAR_INT = '/<int:%s>'
        self.__FLASK_PATH_VAR_STRING = '/<string:%s>'
        self.__FLASK_PATH_VAR_FLOAT = '/<float:%s>'
        self.__FLASK_PATH_VAR_PATH = '/<path:%s>'

        #Class declarations. Mostly for Response bodies
        self.__FLASK_CLASS_DECLARATION = '\nclass %s:'
        self.__FLASK_CLASS_INIT_DEF = '''\n\tdef __init__(self):'''
        self.__FLASK_CLASS_INIT_SELF_INT = '''\n\t\tself.%s = 0'''#%s to have variable name
        self.__FLASK_CLASS_INIT_SELF_STRING = '''\n\t\tself.%s = ""'''
        self.__FLASK_CLASS_INIT_SELF_DATE = '''\n\t\tself.%s = ""'''
        self.__FLASK_CLASS_INIT_SELF_LIST = '''\n\t\tself.%s = []'''
        self.__FLASK_CLASS_INIT_SELF_DICT = '''\n\t\tself.%s = {}'''
        self.__FLASK_CLASS_INIT_IMPORT_SNIPPET = '''\n\timport responses.{class_name} as {class_name}'''

        #Request Parametrs and its validation
        self.__FLASK_DEF_BODY_REQ_PARAM_REQUIRED = '''\n\tassert request.args.get("%s") != None'''
        self.__FLASK_DEF_BODY_REQ_PARAM_REQUIRED_TYPE = '''\n\tassert type(request.args.get("%s")) != %s'''
        self.__FLASK_DEF_BODY_REQ_PARAM_NOT_REQUIRED = '''\n\t#assert request.args.get("%s") != None'''

    def createFile(self, filename, fileLocation):
        if filename is None:
            raise ValueError('Please provie a valid filename')
        if fileLocation is None:
            raise ValueError('Please provide a valid location for the file')
        fullFilePath = os.path.join(fileLocation, filename)
        with open(fullFilePath, 'w') as f:
            f.write('')
            f.close()

    def checkFile(self, filename, fileLocation):
        if filename is None or fileLocation is None:
            raise ValueError('File with the provided name and path does not exist')
        fullFilePath = os.path.join(fileLocation, filename)
        return os.path.isfile(fullFilePath)

    def checkDir(self, dirLocation):
        if dirLocation is None:
            raise ValueError('Provided directory location is not valid')
        if str != type(dirLocation):
            raise ValueError('Provided directory location is not valid')
        if os.path.isdir(dirLocation):
            pass
        else:
            self.makeDir(dirLocation)

    def makeDir(self, dirLocation):
        if dirLocation is None:
            raise ValueError('No valid dir location provided')
        os.mkdir(dirLocation)

    def createControllerFile(self, filename, fileLocation, apis=[]):
        if self.checkFile(filename,fileLocation):
            # raise ValueError('Already existing controller exists')
            pass
        self.checkDir(fileLocation)
        self.createFile(filename, fileLocation) #File created
        if apis is None or apis == []:
            raise ValueError('No API provided to be written in the controller')
        self.writeFileHeader(filename, fileLocation)
        for apiDetail in apis:
            if apiDetail['method'] == None:
                #Give error stating method not passed
                continue
            if apiDetail['method'].lower() == 'get':
                self.writeGETapi(apiDetail, filename, fileLocation)
            elif apiDetail['method'].lower() == 'post':
                self.writePOSTapi(apiDetail, filename, fileLocation)
        self.writeFileFooter(filename, fileLocation)

    def writeFileHeader(self, filename, fileLocation):
        with open(os.path.join(fileLocation,filename), 'w') as fp:
            fp.write(self.__FLASK_HEADER)
            fp.close()

    def writeFileFooter(self, filename, fileLocation):
        with open(os.path.join(fileLocation,filename), 'a') as fp:
            fp.write(self.__FLASK_FOOTER)

    def writeGETapi(self, apiDetail, filename, fileLocation):
        print('Writing GET API: ', apiDetail['name'])
        if apiDetail['path'] == {} or apiDetail['path'] == None:
            route = apiDetail['route']
            method_params = ''
        else:
            route = apiDetail['route']
            method_params = ''
            for i in apiDetail['path']:
                #apiDetail['path'][i] defines the type of the path variable
                if str(apiDetail['path'][i]).lower() == 'int':
                    route += self.__FLASK_PATH_VAR_INT % i
                elif str(apiDetail['path'][i]).lower() == 'string':
                    route +=self.__FLASK_PATH_VAR_STRING % i
                method_params = method_params+str(i)+','
            else:
                method_params = method_params[:-1]

        with open(os.path.join(fileLocation,filename), 'a') as fp:
            fp.write(self.__FLASK_API_GET_ROUTE_HEADER % route)
            fp.write(self.__FLASK_DEF_DECLARATION %(apiDetail['name'], method_params))

            if apiDetail['parameters'] is not None and type(apiDetail['parameters']) is dict:
                for item in apiDetail['parameters'].items():
                    #Gives a list of the parameters
                    #[(name, {type:int, required: true}), (id, {type:string, required:false})]
                    # one item = one tuple
                    if item[1]['required'] == True:
                        fp.write(self.__FLASK_DEF_BODY_REQ_PARAM_REQUIRED % item[0])
                        fp.write(self.__FLASK_DEF_BODY_REQ_PARAM_REQUIRED_TYPE %(item[0],item[1]['type']))
                    else:
                        fp.write(self.__FLASK_DEF_BODY_REQ_PARAM_NOT_REQUIRED % item[0])

            if apiDetail['response_body'] == {} or apiDetail['response_body'] is None:
                fp.write(self.__FLASK_DEF_BODY_WITHOUT_RESPONSE)
            else:
                #Write code to write the class with all the fields for response body and also
                #create an __init__ file so that the file can be imported.
                cfilename = apiDetail['response_body']['name']+'.py'
                self.checkDir(os.path.join(fileLocation,'responses'))
                cf = open(os.path.join((os.path.join(fileLocation,'responses')),cfilename), 'w')
                cf.write(self.__FLASK_CLASS_DECLARATION % apiDetail['response_body']['name'])
                cf.write(self.__FLASK_CLASS_INIT_DEF)
                for response_param in apiDetail['response_body']['fields']:
                    if str == type(apiDetail['response_body']['fields'][response_param]):
                        cf.write(self.__FLASK_CLASS_INIT_SELF_STRING % response_param)
                    elif int == type(apiDetail['response_body']['fields'][response_param]):
                        cf.write(self.__FLASK_CLASS_INIT_SELF_INT % response_param)
                    elif list == type(apiDetail['response_body']['fields'][response_param]):
                        cf.write(self.__FLASK_CLASS_INIT_SELF_LIST % response_param)
                    elif dict == type(apiDetail['response_body']['fields'][response_param]):
                        cf.write(self.__FLASK_CLASS_INIT_SELF_DICT % response_param)
                    else:
                        cf.write(self.__FLASK_CLASS_INIT_SELF_STRING % response_param)
                cf.close()
                self.createFile('__init__.py', os.path.join(fileLocation,'responses'))
                fp.write(self.__FLASK_CLASS_INIT_IMPORT_SNIPPET.format(class_name=str(apiDetail['response_body']['name'])))
                fp.write(self.__FLASK_DEF_BODY_WITH_RESPONSE % (str(apiDetail['response_body']['name'])+'.'+ str(apiDetail['response_body']['name'])))
            

    def writePOSTapi(self, apiDetail, filename, fileLocation):
        print('Writing POST API')
        if apiDetail['path'] == {} or apiDetail['path'] == None:
            route = apiDetail['route']
            method_params = ''
        else:
            route = apiDetail['route']
            method_params = ''
            for i in apiDetail['path']:
                #apiDetail['path'][i] defines the type of the path variable
                if str(apiDetail['path'][i]).lower() == 'int':
                    route += self.__FLASK_PATH_VAR_INT % i
                elif str(apiDetail['path'][i]).lower() == 'string':
                    route +=self.__FLASK_PATH_VAR_STRING % i
                method_params = method_params+str(i)+','
            else:
                method_params = method_params[:-1]
            print (route)
        with open(os.path.join(fileLocation,filename), 'a') as fp:
            fp.write(self.__FLASK_API_POST_ROUTE_HEADER % route)
            fp.write(self.__FLASK_DEF_DECLARATION %(apiDetail['name'], method_params))
            if apiDetail['response_body'] == {} or apiDetail['response_body'] is None:
                fp.write(self.__FLASK_DEF_BODY_WITHOUT_RESPONSE)
            else:
                #Write code to write the class with all the fields for response body and also
                #create an __init__ file so that the file can be imported.
                cfilename = apiDetail['response_body']['name']+'.py'
                self.checkDir(os.path.join(fileLocation,'responses'))
                cf = open(os.path.join((os.path.join(fileLocation,'responses')),cfilename), 'w')
                cf.write(self.__FLASK_CLASS_DECLARATION % apiDetail['response_body']['name'])
                cf.write(self.__FLASK_CLASS_INIT_DEF)
                for response_param in apiDetail['response_body']['fields']:
                    if str == type(apiDetail['response_body']['fields'][response_param]):
                        cf.write(self.__FLASK_CLASS_INIT_SELF_STRING % response_param)
                    elif int == type(apiDetail['response_body']['fields'][response_param]):
                        cf.write(self.__FLASK_CLASS_INIT_SELF_INT % response_param)
                    elif list == type(apiDetail['response_body']['fields'][response_param]):
                        cf.write(self.__FLASK_CLASS_INIT_SELF_LIST % response_param)
                    elif dict == type(apiDetail['response_body']['fields'][response_param]):
                        cf.write(self.__FLASK_CLASS_INIT_SELF_DICT % response_param)
                    else:
                        cf.write(self.__FLASK_CLASS_INIT_SELF_STRING % response_param)
                cf.close()
                self.createFile('__init__.py', os.path.join(fileLocation,'responses'))
                fp.write(self.__FLASK_CLASS_INIT_IMPORT_SNIPPET.format(class_name=str(apiDetail['response_body']['name'])))
                fp.write(self.__FLASK_DEF_BODY_WITH_RESPONSE % (str(apiDetail['response_body']['name'])+'.'+ str(apiDetail['response_body']['name'])))
                fp.close()
