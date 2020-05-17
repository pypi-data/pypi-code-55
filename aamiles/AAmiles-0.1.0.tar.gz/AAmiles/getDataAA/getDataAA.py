import requests
from bs4 import BeautifulSoup
import os

class get:

    def __init__(self):
        '''Descarga la tabla de millas de AA.

        Uso:

        import getDataAA

        data = getDataAA.get()

        data.millas # lista con los valores de millas. 
        data.titles # lista con los titulos de las tablas
        data.destinos # lista con los destinos de las millas

        '''

        headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}

        URL = 'https://www.aerolineas.com.ar/es-ar/aerolineas_plus/disfrutatusmillas'

        self.headers = headers
        self.URL = URL
        
        try:
            self.page = requests.get(self.URL, headers=self.headers)
            self.soup = BeautifulSoup(self.page.content, 'html.parser')

            self.getTitles(['panel-body','table-left-fixed'])
            self.getTables(['table-left-fixed'])
        except ConnectionError:
            print("No hay conexion a internet.")
        except:
            print("Error. Verificar conexion de red.")
                  
    def getTitles(self, clss):
        self.titles = []
        for cl in clss:
            table = self.soup.findAll('div', {'class': cl})
            for tabla in table:
                if tabla.find('h4'):
                    self.titles.append(tabla.find('h4').text.strip())

    def getDestinos(self,tabla, encabezado, row):
    
        destinos = []
        subtable = tabla.find(encabezado)
        rw = subtable.find_all(row)
        destinos = [ele.text.strip() for ele in rw]
        self.destinos.append(destinos)

    def getMillas(self, tabla, encabezado, rowID, colID):
        
        millas = []
        subtable = tabla.find(encabezado)
        rows = subtable.find_all(rowID)
        for row in rows:
            cols = row.find_all(colID)
            cols = [ele.text.strip() for ele in cols]
            millas.append([ele for ele in cols if ele])
        self.millas.append(millas)

    def getTables(self, clss):
        self.destinos = []
        self.millas = []
        for cl in clss:
            table = self.soup.findAll('div', {'class': cl})
            for tabla in table:
                self.getDestinos(tabla,'thead','th')
                self.getMillas(tabla,'tbody','tr','td')