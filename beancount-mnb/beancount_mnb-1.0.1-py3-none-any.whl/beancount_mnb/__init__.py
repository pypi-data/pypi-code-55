from decimal import Decimal
import pytz
from beancount.prices import source
from datetime import datetime
from zeep import Client
from lxml import etree

__version__ = '1.0.1'


class Source(source.Source):
    def get_latest_price(self, ticker):
        mnb_client = get_mnb_client()
        # ez tartalmazza az aznapi összes devizát
        mnb_result = mnb_client.service.GetCurrentExchangeRates()
        return parse_mnb_result(mnb_result, ticker)

    def get_historical_price(self, ticker, time):
        mnb_client = get_mnb_client()
        # ez csak a kért devizát tartalmazza
        mnb_result = mnb_client.service.GetExchangeRates(time, time, ticker)
        return parse_mnb_result(mnb_result, ticker)


def get_mnb_client():
    """zeep SOAP kliens visszaadása"""
    return Client('http://www.mnb.hu/arfolyamok.asmx?wsdl')


def parse_mnb_result(mnb_result, ticker):
    """Válasz XML feldolgozása, átalakítása a beancount által elvárt beancount.prices.source.SourcePrice() formátumra

    <MNBCurrentExchangeRates>
        <Day date="2019-02-22">
            <Rate unit="1" curr="AUD">199,16000</Rate>
            <Rate unit="1" curr="BGN">162,51000</Rate>
        </Day>
    </MNBCurrentExchangeRates>
    """
    # kézi XML feldolgozás, mert az MNB lusta volt XSD sémát mellékelni a servicehez
    root = etree.fromstring(mnb_result)
    if len(root) > 0:
        # ha a fa gyökerének van eleme (<Day>), dátum feldolgozása
        datum = datetime.strptime(root[0].attrib['date'], '%Y-%m-%d').replace(tzinfo=pytz.timezone('CET'))
        # végigmegyünk a <Rate> elemeken
        for currency in root[0]:
            if currency.attrib['curr'] == ticker:
                # ha a kért árfolyam devizaneme megfelel, árfolyam konvertálása 1 egységre
                arfolyam = Decimal(currency.text.replace(',', '.'))
                egyseg = int(currency.attrib['unit'])
                return source.SourcePrice(price=Decimal(arfolyam / egyseg), time=datum, quote_currency='HUF')
    else:
        # ha az xml fa gyökerének nincs eleme, akkor aznapra nincs érvényes árfolyam
        return source.SourcePrice(price=None, time=datetime.now(tz=pytz.timezone('CET')), quote_currency='HUF')
