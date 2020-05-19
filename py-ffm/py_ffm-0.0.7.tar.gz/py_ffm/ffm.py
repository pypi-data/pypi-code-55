import mimetypes
import base64
from io import BytesIO
from ftplib import FTP
import os


class FtpFileManager():
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def documentDownload(self, filepath, filename):
        ftp = FTP(self.host)
        ftp.login(self.username, self.password)
        ftp.cwd(filepath + '/')
        
        r = BytesIO()
        ftp.retrbinary('RETR '+ filename, r.write)
        item = base64.b64encode(r.getvalue()).decode()

        gFile = open(filename, "wb")
        ftp.retrbinary('RETR '+ filename, gFile.write)
        gFile.close()
        ftp.close()
        return {'data': item, 'mimetype': mimetypes.guess_type(filename)[0]}

    def documentDelete(self, filename):
        os.remove(filename)
        return {'message': 'File deleted.'}

    def documentDownloadDelete(self, filepath, filename):
        ftp = FTP(self.host)
        ftp.login(self.username, self.password)
        ftp.cwd(filepath + '/')
        
        r = BytesIO()
        ftp.retrbinary('RETR '+ filename, r.write)
        item = base64.b64encode(r.getvalue()).decode()

        gFile = open(filename, "wb")
        ftp.retrbinary('RETR '+ filename, gFile.write)
        gFile.close()
        ftp.close()
        os.remove(filename)
        return {'data': item, 'mimetype': mimetypes.guess_type(filename)[0]}
        
        
    def postRegistry(self, filepath, dirname):
        ftp = FTP(self.host)
        ftp.login(self.username, self.password)
        ftp.cwd(filepath)
        files = []
        ftp.retrlines('LIST', files.append)
        if len(files) == 0:
            ftp.mkd(dirname)
            filePath = filepath + '/' + dirname
            return {'message':'Sikeres létrehozás', 'path': filePath }
        else:
            for f in files:
                if f.split()[-1] == dirname and f.upper().startswith('D'):
                    return {'error':'Létező könyvtár!'}, 300
                else:
                    ftp.mkd(dirname)
                    filePath = filepath + '/' + dirname
                    return {'message':'Sikeres létrehozás', 'path': filePath }


    def getDocuments(self, filepath):
        ftp = FTP(self.host)
        ftp.login(self.username, self.password)      
        ftp.cwd(filepath)
        files = []
        ftp.retrlines("LIST", files.append)

        return files

    def postDocuments(self, filepath, file, filename):
        #for file in request.files.getlist('file'):
        #filename = file.filename
        ftp = FTP(self.host)
        ftp.login(self.username, self.password)
        ftp.cwd(filepath)
        ftp.storbinary('STOR ' + filename, fp=file)
        ftp.quit()
        
        return {'msg': 'success'}
        
    def deleteDocuments(self, filepath, filenames):
        filenames = filenames
        ftp = FTP(self.host)
        ftp.login(self.username, self.password)
        ftp.cwd(filepath)
        filelist = ftp.nlst()
        for filen in filenames:
            for file in filelist:
                if file == filen:
                    ftp.delete(file)
        return {'msg': 'Success'}
