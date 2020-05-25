from bs4 import BeautifulSoup
import urllib.request
import logging

class IPCA():

    def __init__(self, url="https://sidra.ibge.gov.br/home/ipca/brasil#"):
        self.URL = url
        self.logger = logging.getLogger('indicis')

    def crawler(self):
        try:
            resp = urllib.request.urlopen(self.URL)
            resp_bytes = resp.read()
            html_as_string= resp_bytes.decode("utf8")

            soup = BeautifulSoup(html_as_string)
            table = soup.find('table' , attrs={'class': 'quadro' })
            title_date =  table.findAll('tr')[1].findAll("th")[0].get_text()
            title =  table.findAll('tr')[3].findAll("th")[0].get_text()
            if title == "Índice geral":
                date = self._extract_date(title_date)
                mensal = table.findAll('tr')[3].findAll("td")[0].get_text()
                anual =  table.findAll('tr')[3].findAll("td")[1].get_text()
                return date,mensal,anual
            else:
                return None

        except Exception as e:
            self.logger.error('IPCA no available')
            self.logger.error(e)
            return

    def _extract_date(self, title):  
        date_text = title[9:]     
        date_parts = date_text.split()
        month = date_parts[0]
        year = date_parts[1]

        MONTHS = {'janeiro':1, 'fevereiro':2,'março':3,'abril':4, 'maio':5, 'junho':6, 'julho':7, 'agosto':8, 'setembro':9, 'outubro':10, 'novembro':11, 'dezembro':12}
        return "{:02d}/{}".format(MONTHS[month], year)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ipca = IPCA()
    ipca_mensal, ipca_anual,title_date = ipca.crawler()
    print(ipca_mensal, ipca_anual, title_date)