import csv
import ipaddress
import json
import sqlite3
import shutil
from itertools import groupby
from os import path, makedirs


def clean(value):
    """Strip trailing whitespaces and quotes."""
    return value.strip(' "')


class LocationPacker:
    """GeoIP Location Packer.

    Extracts data from the various database files, and generates a series of files that the Rig UI
    and the Platform can use.

    The database is the MaxMind GeoIP2 CSV Databases (City and Country).
    See https://dev.maxmind.com/geoip/geoip2/geoip2-city-country-csv-databases/
    """
    encoding = 'utf-8'

    def __init__(self, db_path, data_dir, version):
        self.db_path = path.normpath(db_path)
        self.version = version
        self.data_dir = path.join(path.normpath(data_dir), self.version)

        self.areas = []
        self.countries = {}  # This will hold the final JSON payload
        self.geoname_country_map = {}
        self.ipv4_map = []
        self.ipv6_map = []

    def __call__(self):
        # Wipe out the destination folder.
        if path.exists(self.data_dir):
            shutil.rmtree(self.data_dir)
        makedirs(path.join(self.data_dir, 'countries'))

        # Parse GeoIP database files.
        try:
            self.read_countries()
            self.read_cities()
            self.read_ip_addresses()
        except (FileNotFoundError, TypeError):
            raise SystemExit

        # Unpack.
        self.unpack()

        # Generate SQLite3 database.
        self.create_database()

    def create_database(self):
        """Create the areas and iplookup sqlite3 databases."""

        # De-duplicated area labels
        self.areas = sorted(self.areas, key=lambda x: (x['country'], x['label'], x['region']))

        areas = []
        for item, _ in groupby(self.areas, lambda x: (x['country'], x['label'], x['region'])):
            areas.append({
                'country': item[0],
                'label': item[1],
                'region': item[2],
            })

        area_db = path.join(self.data_dir, 'areas.db')
        with sqlite3.connect(area_db) as conn:
            c = conn.cursor()
            c.execute('CREATE TABLE label (country text, label text, region text)')
            c.executemany(
                'INSERT INTO label (country, label, region) VALUES (?, ?, ?)',
                [(area['country'], area['label'], area['region']) for area in areas]
            )
            conn.commit()

        iplookup_db = path.join(self.data_dir, 'iplookup.db')
        with sqlite3.connect(iplookup_db) as conn:
            c = conn.cursor()
            c.execute('CREATE TABLE ipv4_lookup (network text, country text, first_ip_string text, '
                      'last_ip_string text, first_ip_int integer, last_ip_int integer)')
            c.executemany(
                'INSERT INTO ipv4_lookup (network, country, first_ip_string, last_ip_string, '
                'first_ip_int, last_ip_int) VALUES (?, ?, ?, ?, ?, ?)',
                [(ip_range['network'], ip_range['country'], ip_range['first_ip_string'],
                  ip_range['last_ip_string'], ip_range['first_ip_int'], ip_range['last_ip_int']) for
                 ip_range in self.ipv4_map]
            )
            c.execute('CREATE TABLE ipv6_lookup (network text, country text, first_ip_string text, '
                      'last_ip_string text, first_ip_int text, last_ip_int text)')
            # because converted ipv6 addresses are too long for SQLITE3 integer fields, we store
            # them as text. Comparison queries still work
            c.executemany(
                'INSERT INTO ipv6_lookup (network, country, first_ip_string, last_ip_string, '
                'first_ip_int, last_ip_int) VALUES (?, ?, ?, ?, ?, ?)',
                [(ip_range['network'], ip_range['country'], ip_range['first_ip_string'],
                  ip_range['last_ip_string'], str(ip_range['first_ip_int']),
                  str(ip_range['last_ip_int'])) for ip_range in self.ipv6_map]
            )
            conn.commit()

    def read_cities(self):
        """Read the region and city from the 'GeoIP2-City-Locations-en.csv' file.

         - Add region codes (subdivisions) to countries.
         - Set areas.
         - Must be read after countries.

        """
        database = path.join(self.db_path, 'GeoIP2-City-Locations-en.csv')
        with open(database, encoding=self.encoding) as fd:
            reader = csv.DictReader(fd)
            for row in reader:

                # Skip entries with no city.
                if not row['city_name']:
                    continue

                # Case 1: both sub-divisions are present; the region code is compiled from both
                # codes, separated by a dot (i.e.: '<sd1_code>.<sd2_code>'); the second division
                # name is used as the region name, with the first division in brackets.
                if row['subdivision_1_iso_code'] and row['subdivision_2_iso_code']:
                    region_code = '{}.{}'.format(
                        row['subdivision_1_iso_code'], row['subdivision_2_iso_code'])
                    region_name = '{} ({})'.format(
                        row['subdivision_2_name'], row['subdivision_1_name'])

                # Case 2: only the first sub-division is filled in; we just use that for region
                # code and name.
                elif row['subdivision_1_iso_code']:
                    region_code = row['subdivision_1_iso_code']
                    region_name = row['subdivision_1_name']

                # Case 3: no sub-divisions at all. We create a dummy 'Unspecified Region' region
                # with code 'N/A'.
                else:
                    region_code = 'N/A'
                    region_name = 'Unspecified Region'

                if region_code not in self.countries[row['country_iso_code']]['regions']:
                    self.countries[row['country_iso_code']]['regions'][region_code] = {
                        'name': region_name,
                        'cities': set([row['city_name']]),
                    }
                else:
                    self.countries[row['country_iso_code']]['regions'][
                        region_code
                    ]['cities'].add(row['city_name'])

                # Add each region to the list of areas.
                # Ignore the 'Unspecified Region' labels.
                if region_code != 'N/A':
                    self.areas.append({
                        'country': row['country_iso_code'],
                        'label': region_name,
                        'region': region_code
                    })

    def read_countries(self):
        """Read the country code and name from the 'GeoIP2-Country-Locations-en.csv' file.

         - Set initial countries.
         - Must be read before cities.

        """
        database = path.join(self.db_path, 'GeoIP2-Country-Locations-en.csv')
        with open(database, encoding=self.encoding) as fd:
            reader = csv.DictReader(fd)
            for row in reader:
                country = clean(row['country_iso_code'])
                if country:
                    self.countries[country] = {
                        'name': clean(row['country_name']),
                        'regions': {},
                    }
                    # other CSVs only refer to country by its geoname_id, so we build
                    # a map of all ids to countries for easier handling
                    self.geoname_country_map[clean(row['geoname_id'])] = country

    def read_ip_addresses(self):
        """Read the ip address """
        database = path.join(self.db_path, 'GeoIP2-Country-Blocks-IPv4.csv')
        with open(database, encoding=self.encoding) as fd:
            reader = csv.DictReader(fd)
            for row in reader:
                cidr_ip_range = clean(row['network'])

                if cidr_ip_range:
                    # attempt to resolve the range to a range, then extract the first and last
                    # ip from that range
                    n = ipaddress.IPv4Network(cidr_ip_range)
                    first, last = n[0], n[-1]

                    # convert the IP to an int at this point, as when it's in the DB it'll make
                    # ip lookup much easier.
                    self.ipv4_map.append({
                        'network': cidr_ip_range,
                        'country': self.geoname_country_map.get(
                            clean(row['registered_country_geoname_id']),
                            ''
                        ),
                        'first_ip_string': str(first),
                        'last_ip_string': str(last),
                        'first_ip_int': int(first),
                        'last_ip_int': int(last),
                    })

        database = path.join(self.db_path, 'GeoIP2-Country-Blocks-IPv6.csv')
        with open(database, encoding=self.encoding) as fd:
            reader = csv.DictReader(fd)
            for row in reader:
                cidr_ip_range = clean(row['network'])

                if cidr_ip_range:
                    n = ipaddress.IPv6Network(cidr_ip_range)
                    first, last = n[0], n[-1]

                    # convert the IP to an int at this point, as when it's in the DB it'll make
                    # ip lookup much easier.
                    self.ipv6_map.append({
                        'network': cidr_ip_range,
                        'country': self.geoname_country_map.get(
                            clean(row['registered_country_geoname_id']),
                            ''
                        ),
                        'first_ip_string': str(first),
                        'last_ip_string': str(last),
                        'first_ip_int': int(first),
                        'last_ip_int': int(last),
                    })

    def unpack(self):
        """Convert GeoIP locations to JSON files."""

        # Output country list (geo.json)
        # Note that countries are grouped using their names, not their codes.
        # ------------------------------
        # Format:
        #   {
        #     "categories": [
        #       {
        #         "sub": [
        #           {
        #             "value": "<country_code>",
        #             "label": "<country_name>"
        #           },
        #           ...
        #         ],
        #         "label": "<country_name>[:1]",
        #         "value": "<country_name>[:1]"
        #       },
        #       ...
        #     ]
        #   }
        #

        # Order countries dictionary by country name
        sorted_by_name = sorted(self.countries.items(), key=lambda kv: kv[1]['name'])
        self.countries = dict(sorted_by_name)

        categories = []
        for code, value in self.countries.items():
            letter = value['name'][:1]
            try:
                category = [cat for cat in categories if cat['value'] == letter][0]
            except IndexError:
                categories.append({
                    'sub': [{
                        'label': value['name'],
                        'value': code
                    }],
                    'label': letter,
                    'value': letter,
                })
            else:
                categories[categories.index(category)]['sub'].append({
                    'label': value['name'],
                    'value': code
                })

        output = {'categories': categories}

        with open(path.join(self.data_dir, 'geo.json'), mode='w', encoding='utf-8') as fd:
            fd.write(json.dumps(output, indent=2))

        # Create country files (countries/<country_code>.json)
        # ------------------------------
        # Format:
        #   {
        #     "categories": [
        #       {
        #         "country": "<country_code>",
        #         "value": "<region_code>",
        #         "label": "<region_name>",
        #         "sub": [
        #           {
        #             "value": "<city>",
        #             "label": "<city>"
        #           },
        #           ...
        #         ]
        #       },
        #       ...
        #     ]
        #   }
        #
        for country_code, country in self.countries.items():
            output = {
                'categories': [
                    {
                        'country': country_code,
                        'label': region['name'],
                        'value': code,
                        'sub': [
                            {
                                'label': city,
                                'value': city
                            }
                            for city in sorted(region['cities'])
                        ],
                    }
                    for code, region in sorted(country['regions'].items())
                ]
            }

            country_file = path.join(self.data_dir, 'countries', country_code + '.json')
            with open(country_file, mode='w', encoding='utf-8') as fd:
                fd.write(json.dumps(output))
