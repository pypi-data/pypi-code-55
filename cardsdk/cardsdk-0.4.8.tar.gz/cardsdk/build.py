#-*-coding:utf-8-*-
from .util import *
import shutil,json 

class Build:
    def envCheck(self):
        cui.w('CHECK UPGRADE START....')
        #env
        setupEnv()

    def buildTask(self,dir,out,biz):
        print('\r\n')
        cui.w('BUILD TASK START....')

        entry = dir
        bizCode = biz
        outPath = out
        outPathZip = os.path.join(outPath,'zip')

        if os.path.exists(outPath):
            shutil.rmtree(outPath)
    
        cui.i('outPath is {0}'.format(outPath))
        cui.i('outPathZip is {0}'.format(outPathZip))
    
        buildCommand = "accore1 build -p {0} -d {1}".format(entry,'./temp')
        buildEnd = os.system(buildCommand)
        if buildEnd == 0:
            #mk output dir 
            if not os.path.exists(outPath) :
                os.makedirs(outPath)
                os.makedirs(outPathZip)
            #process bin
            binResult = getAllFtFiles('./temp','.bin')
            for binPath in binResult:
                filePath,filename=os.path.split(binPath)
                #read json
                filename,donotcare = os.path.splitext(filename)
                jsonPath = os.path.join(filePath,filename+'.json')
            
                with open(jsonPath,'r') as jsonFile:
                    jsonFileContent = jsonFile.read()

                jsonDic = json.loads(jsonFileContent)
                metaString = jsonDic['meta']
                meta = json.loads(metaString)
                version = meta['version']
                templateId = meta['name']
                # build template
                tplRenamePath = "{0}@{1}@{2}.template".format(bizCode,templateId,version)
                os.rename(binPath,outPath + '/' + tplRenamePath)
                # build zst
                zstdPath= os.path.join(filePath,filename+'.zst')
                zstrenamePath = "{0}@{1}@{2}.zip".format(bizCode,templateId,version)
                os.rename(zstdPath,outPathZip + '/'+ zstrenamePath)
                cui.s('MD5'+'('+zstrenamePath+'):' + zsmd5(outPathZip + '/'+ zstrenamePath))
        shutil.rmtree('./temp')
        cui.w('BUILD TASK  END....')
