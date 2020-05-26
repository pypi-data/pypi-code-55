import re
import os.path


pkg_dir = os.path.abspath(os.path.dirname(__file__))

ASN_FILE = os.path.join(pkg_dir, 'data', 'GeoLite2-ASN.mmdb')
CITY_FILE = os.path.join(pkg_dir, 'data', 'GeoLite2-City.mmdb')
COUNTRY_FILE = os.path.join(pkg_dir, 'data', 'GeoLite2-Country.mmdb')