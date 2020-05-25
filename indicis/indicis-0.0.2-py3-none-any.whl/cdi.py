import urllib.request
import logging

class CDI():

    def __init__(self, ftp_cdi="ftp://ftp.cetip.com.br/MediaCDI/"):
        self.URL = ftp_cdi
        self.logger = logging.getLogger('indicis')

    def crawler(self, year, month, day):
        date = "{}{:02d}{:02d}".format(year,month,day)
        url = "{}{}.txt".format(self.URL,date)
        try:
            self.logger.debug(" Buscar cdi em "+url)
            data = urllib.request.urlopen(url)
            di=float(data.read())
            return di/100.0
        except Exception as e:
            self.logger.error('CDI no available at'+date)
            self.logger.error(e)
            return

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    cdi = CDI()
    di = cdi.crawler(2020,5,25)
    print(di)