import requests
import io
import zipfile
import re
from bs4 import BeautifulSoup
import logging

class DIFuturo():
    def __init__(self, url="http://www.b3.com.br/pesquisapregao/download?filelist=PR{}.zip"):
        self.URL_TEMPLATE=url
        self.disFuturo = {}
        self.daps = {}
        self.logger = logging.getLogger('indicis')

    def crawler(self,year, month, day):
        url = self._format_url(year, month, day)
        _, content = self._load_remote_file(url)
        self._process_zip(content)
        return self.disFuturo

    def _process_zip(self,content):
        with zipfile.ZipFile(content) as rootZip:
            for zipinfo in rootZip.infolist():
                with rootZip.open(zipinfo):
                    self.logger.debug("--IPN zip content " + zipinfo.filename)
                    if re.search(r'\.zip$', zipinfo.filename) != None:
                        self.logger.debug("---- Reading " + zipinfo.filename)
                        internalZip = io.BytesIO(rootZip.read( zipinfo.filename))
                        with zipfile.ZipFile(internalZip) as zf:
                            for name in zf.namelist():
                                self.logger.debug("------ Found internal file: " + name)
                                self.logger.debug("------ Processing XML")                                
                                self._processar_xml(zf, name)  
                                if len(self.disFuturo) > 0 and len(self.daps) > 0:                                   
                                    return self.disFuturo

    def _format_url(self,year, month, day):
        date = "{}{:02d}{:02d}".format(year,month,day)[2:]
        return self.URL_TEMPLATE.format(date)

    def _load_remote_file(self, url):   
            response = requests.get(url)
            if response.status_code != 200 :
                self.logger.error("IPN file not founded, raise erro")
                raise ValueError("ipn file not found to url " + url)
            else:
                self.logger.debug("ipn zip downloaded")
            return response.status_code, io.BytesIO(response.content)

    def _processar_xml(self, zf, name2):
        with zf.open(name2) as fxml:
            xml = fxml.read()
            soup = BeautifulSoup(xml,'lxml')
            self._extrair_indice(soup)  

    def _extrair_indice(self, soup):
        lstPricrpt = soup.findAll('pricrpt')
        for pricrpt in lstPricrpt:
            tckrsymb = pricrpt.find('tckrsymb')
            tckrsymbtext = tckrsymb.get_text().strip()

            if tckrsymbtext.startswith("DI1"):
                self.logger.debug("--------" + tckrsymbtext)
                adjstdqttax = pricrpt.find('adjstdqttax')
                if adjstdqttax :
                    self.logger.debug("--------" + adjstdqttax.get_text() + "%")
                    self.disFuturo[tckrsymbtext] = adjstdqttax.get_text()
            elif tckrsymbtext.startswith("DAP"):
                self.logger.debug("--------" + tckrsymbtext)
                adjstdqttax = pricrpt.find('adjstdqttax')
                if adjstdqttax :
                    self.logger.debug("--------"+adjstdqttax.get_text()+"%")
                    self.daps[tckrsymbtext] = adjstdqttax.get_text()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    diFuturo = DIFuturo()
    di = diFuturo.crawler(2020,5,21)
    print(di)