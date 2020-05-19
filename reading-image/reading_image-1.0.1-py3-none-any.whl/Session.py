from .Processed import Processed

import requests

class Session:
    """
    Session objects are used to interact with the readingimage.com server. All interactions with Reading Image are
    through the Session object. This is initialised by passing through the user specific Python Key that is available
    after registering.
    ...

    Attributes
    ----------
    HOME_URL : str
        The homepage of Reading Image, i.e. http://www.readingimage.com/
    session : requests.Session()
        Session object used to call server

    Methods
    -------
    getDemos()
        Retrieves the latest demo Processed objects from Reading Image server
    getAnalysis()
        Retrieves pre-analysed Processed objects from Reading Image server
    analyseFile()
        Send a new file to Reading Image server for analysis
    saveAnalysis():
        Save a reading_image.Procesed object to the Reading Image server
    listFolders()
        Retrieves a list of saving folders from Reading Image server
    listSaved()
        Retrieves a list of meta-date for analysed files from Reading Image server
    """

    HOME_URL = r"http://www.readingimage.com/"

    def __init__(self, python_key=''):
        """Initialise reading_image.Session.

        Args:
            python_key (str): Unique user reference key
        """

        if python_key != '':
            self._python_key = str(python_key)
        else:
            raise ValueError(
                "python_key is a required argument. You can obtain your python key by logging into " +
                "your profile section on readingimage.com"
            )

        self._session = requests.Session()

    @property
    def session(self):
        """Session object used to call server
        """
        return self._session

    def _get(self, url, args=""):

        try:
            response = self.session.get(
                "{}python/{}/{}/{}".format(self.HOME_URL, url, self._python_key, args)
            )
        except:
            raise

        return response

    def _post(self, url, filepath = None, data = {}):

        _files = {'fileupload': open(filepath,'rb')} if filepath else {}

        try:
            response = self.session.post(
                "{}python/{}/{}/".format(self.HOME_URL, url, self._python_key),
                files = _files,
                data = data
            )
        except:
            raise

        return response

    def getDemos(self):
        """Retrieves the latest demo Processed objects from Reading Image server.

        Returns:
            list: a list of reading_image.Processed objects for each demo file
        """

        resp = self._get("get_demos")
        if resp.status_code == 200:
            return [
                Processed(name = demoname, json_response = demodata)
                for demoname, demodata in eval(self._get("get_demos").text).items()
            ]
        else:
            raise ValueError("Status code error from readingimage.com. Server returned {}".format(resp.status_code ))

    def getAnalysis(self, file_ref = None):
        """Retrieves pre-analysed Processed objects from Reading Image server.

        Args:
            file_ref (str): Unique reference code for a processed file

        Returns:
            reading_image.Processed: object holding analysis data
        """

        resp = eval(self._get("get_analysis", args=file_ref).text)

        return Processed(name = resp["name"], json_response = resp["data"])

    def _listAnalysed(self):

        resp = self._get("list_analysed").text

        resp = resp.replace("null", "None")
        resp = resp.replace("false", "False")
        resp = resp.replace("true", "True")

        return eval(resp)

    def analyseFile(self, filepath: str, advanced_ocr: bool = False, translation: bool = False):
        """Send a new file to Reading Image server for analysis.

        Args:
            filepath (str): Location of the file to be processed
            advanced_ocr (bool): Flag to indicate the use of Advance OCR to look for tables. Default is False.
            translation (bool): Flag to indicate the use of Translation (English from French). Default is False.

        Returns:
            reading_image.Processed: object holding analysis data
        """

        processes = []
        if advanced_ocr: processes.append("checkbox_adocr")
        if translation: processes.append("checkbox_translation")

        resp = eval(self._post("analyse_file", filepath=filepath, data={"checkbox_process": processes}).text)

        return Processed(name = resp["name"], json_response = resp["data"])

    def saveAnalysis(self, processed_object, file_name, folder_name):
        """Save a reading_image.Procesed object to the Reading Image server.

        Args:
            processed_object (reading_image.Processed): Object to be saved
            file_name (str): User defined name for file
            folder_name (str): Folder location to save to

        Returns:
            str: server response message
        """

        data = {
            "processed_ref": processed_object.name,
            "file_name": file_name,
            "folder_name": folder_name
        }

        resp = self._post("save_analysis", filepath = None, data = data)

        return resp.text

    def listFolders(self):
        """Retrieves a list of saving folders from Reading Image server.

        Returns:
            list: a list (of str) of folder name
        """

        resp = self._get("list_folders")

        return resp.text

    def listSaved(self):
        """Retrieves a list of meta-date for analysed files from Reading Image server.

        Returns:
            list: a list (of dict) of meta-data for each saved analysed file
        """

        return [f for f in self._listAnalysed() if f["folder"] != None]