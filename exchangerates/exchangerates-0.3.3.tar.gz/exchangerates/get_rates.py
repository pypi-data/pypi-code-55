import csv
import requests
import datetime
import re
import json
import os

from lxml import etree

from .util import fred_countries_currencies, oecd_countries_currencies


OECD_RATES = "http://stats.oecd.org/restsdmx/sdmx.ashx/GetData/MEI_FIN/CCUS.AUS+AUT+BEL+CAN+CHL+CZE+DNK+EST+FIN+FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LVA+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP+SWE+CHE+TUR+GBR+USA+EA19+SDR+NMEC+BRA+CHN+COL+CRI+IND+IDN+RUS+ZAF.M/all?startTime=1950-01"

FRED_CATEGORY_API = "https://api.stlouisfed.org/fred/category/series?category_id={}&api_key={}&file_type=json"
FRED_SERIES_OBSERVATIONS_API = "https://api.stlouisfed.org/fred/series/observations?series_id={}&api_key={}&file_type=json"
FRED_DAILY_CATEGORY = 94


def get_fred_rates(outfp, writer):
    def get_rates(id_, from_currency, to_currency, freq, attempt=1, max_attempts=5):
        print("Retrieving rates from FRED for {}".format(id_))
        while attempt <= max_attempts:
            try:
                get_rates_attempt(id_, from_currency, to_currency, freq)
                break
            except json.decoder.JSONDecodeError as inst:
                if attempt == max_attempts:
                    print("Failed retrieving rates for that currency after {} attempts.".format(attempt))
                    raise
                attempt += 1
                print("Could not retrieve rates for that currency, retrying (attempt {})...".format(attempt))
                pass


    def get_rates_attempt(id_, from_currency, to_currency, freq):
        r_series = requests.get(FRED_SERIES_OBSERVATIONS_API.format(id_, os.environ['FRED_API_KEY']))
        r_series_json = r_series.json()
        if r_series_json['count'] > r_series_json['limit']:
            raise
        country = {True: to_currency,
                   False: from_currency}[from_currency == "U.S."]
        print("Getting data for currency {}".format(fred_countries_currencies[country]))
        for row in r_series_json['observations']:
            if row['value'] == ".":
                continue
            if from_currency == "U.S.":
                row['value'] = 1/float(row['value'])
            outrow = [row['date'], row['value'], fred_countries_currencies[country], freq, "FRED"]
            writer.writerow(outrow)

    def retrieve_rates():
        r = requests.get(FRED_CATEGORY_API.format(FRED_DAILY_CATEGORY, os.environ['FRED_API_KEY']))
        categories_json = r.json()
        for series in categories_json["seriess"]:
            # We only want real daily exchange rates
            if not series['id'].startswith("DEX"):
                continue
            from_currency, to_currency = re.match(
                    "(.*) / (.*) Foreign Exchange Rate", series['title']
                    ).groups()
            freq = series['frequency_short']
            try:
                get_rates(series['id'], from_currency, to_currency, freq)
            except Exception as inst:
                print(series['id'])
                raise

    retrieve_rates()


def get_oecd_rates(outfp, writer, include_all_dates):
    def make_date(value):
        return datetime.datetime.strptime(value, "%Y-%m-%d")

    # Find earliest data for each currency from the St Louis Fed data
    def get_earliest_dates():
        outfp_file = open(outfp, "r")
        reader = csv.DictReader(outfp_file)
        indata = list(map(lambda row: row, reader))
        outfp_file.close()

        currencies = dict(map(lambda row: (row["Currency"], None), indata))

        for currency in currencies:
            filtered_currencies = filter(lambda x: x['Currency'] == currency, indata)
            currency_dates = list(map(lambda y:
                      make_date(y["Date"]),
                    filtered_currencies
            ))
            currencies[currency] = min(currency_dates)
        return currencies

    def get_OECD_data(writer, currencies_dates):
        r = requests.get(OECD_RATES)
        fp_doc = etree.fromstring(r.content)
        nsmap = {
            "ns": "http://www.SDMX.org/resources/SDMXML/schemas/v2_0/generic"
        }
        series = fp_doc.findall("ns:DataSet/ns:Series", namespaces=nsmap)
        for serie in series:
            currency = serie.find("ns:SeriesKey/ns:Value[@concept='LOCATION']", namespaces=nsmap).get("value")

            min_currency_date = currencies_dates.get(
                oecd_countries_currencies.get(currency),
                datetime.datetime.utcnow())

            for obs in serie.findall("ns:Obs", namespaces=nsmap):
                date = "{}-01".format(obs.find("ns:Time", namespaces=nsmap).text)
                value = obs.find("ns:ObsValue", namespaces=nsmap).get("value")
                if include_all_dates or (make_date(date) < min_currency_date):
                    writer.writerow([date, value, oecd_countries_currencies.get(currency), "M", "OECD"])

    print("Getting rates from OECD")
    currencies_dates = get_earliest_dates()
    get_OECD_data(writer, currencies_dates)


def update_rates(out_filename, include_all_dates=True):
    if 'FRED_API_KEY' not in os.environ:
        raise Exception("""

    Could not find FRED API key.
    Please get an API key from https://research.stlouisfed.org/useraccount/apikey
    Then set the environment variable using e.g. EXPORT FRED_API_KEY=YOUR-API-KEY.
    """)
    outfp = out_filename
    outfp_f = open(outfp, 'w')
    writer = csv.writer(outfp_f)
    writer.writerow(['Date', 'Rate', 'Currency', 'Frequency', 'Source'])
    get_fred_rates(outfp, writer)
    outfp_f.close()

    outfp_f = outfp_f = open(outfp, 'a')
    writer = csv.writer(outfp_f)
    get_oecd_rates(outfp, writer, include_all_dates)
    outfp_f.close()


if __name__ == "__main__":
    update_rates('data/consolidated_rates.csv')
