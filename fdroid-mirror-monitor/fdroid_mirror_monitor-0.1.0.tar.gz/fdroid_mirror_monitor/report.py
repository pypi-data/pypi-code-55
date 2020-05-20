#!/usr/bin/env python3

# internal:
from fdroid_mirror_monitor.repo import infos_from_jar
# stdlibs
from datetime import datetime
from urllib.parse import urlparse
import json
import os
import re
import requests
import shutil
import socket
import ssl
import subprocess
import tempfile
# external:
from fdroidserver import common, index
import dns.resolver
import GeoIP
import yaml


def create(repo_url, repo_details=False, timeout=60, headers={'User-Agent': 'F-Droid'},
                  fingerprint='43238D512C1E5EB2D6569F4A3AFBF5523418B82E0A3ED1552770ABB9A9C9CCAB'):
    """
    Run multiple tests:
    - name (hostname)
    - url
    - errors{}
    - IPv4[], IPv6[]
    - repo{}
    - status
    - headers{}
    - starttime
    - duration
    - TLS
    - tlsping{}
    - tls_details{}

    :param repo_url: url of repo/mirror
    :return: the report as dict
    """

    config = dict()
    config['jarsigner'] = 'jarsigner'
    common.config = config
    index.config = config

    print('Checking', repo_url)
    report = dict()
    data = None
    hostname = urlparse(repo_url).hostname
    report['name'] = hostname
    report['url'] = repo_url
    report['errors'] = dict()

    # Get all ip addresses and corresponding countries from DNS
    if not hostname.endswith('.onion'):
        gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
        gi6 = GeoIP.open("/usr/share/GeoIP/GeoIPv6.dat", GeoIP.GEOIP_STANDARD)
        countries = []
        country_codes = []

        try:
            ipv6 = dns.resolver.query(hostname, 'AAAA')
        except dns.resolver.NoAnswer:
            ipv6 = []
        except Exception as e:
            report['errors']['IPv6'] = str(e)

        try:
            ipv4 = dns.resolver.query(hostname, 'A')
        except dns.resolver.NoAnswer:
            ipv4 = []
        except Exception as e:
            report['errors']['IPv4'] = str(e)

        report['IPv4'] = []
        for ip in ipv4:
            report['IPv4'].append(ip.to_text())
            countries.append(gi.country_name_by_addr(ip.to_text()))
            country_codes.append(gi.country_code_by_addr(ip.to_text()))

        report['IPv6'] = []
        for ip in ipv6:
            report['IPv6'].append(ip.to_text())
            countries.append(gi6.country_name_by_addr_v6(ip.to_text()))
            country_codes.append(gi6.country_code_by_addr_v6(ip.to_text()))

        # remove duplicates
        report['countries'] = list(set(countries))
        report['country_codes'] = list(set(country_codes))

    if repo_url.startswith('https://'):
        # speedtest
        success = False
        starttime = datetime.now().timestamp()
        try:
            with requests.get(repo_url + '/index-v1.jar', stream=True, headers=headers, timeout=timeout) as r:
                if r.status_code == 200:
                    with tempfile.NamedTemporaryFile(delete=False) as fp:
                        shutil.copyfileobj(r.raw, fp)
                        success = True
        except Exception as e:
            print(e)
            report['errors']['duration'] = str(e)

        report['duration'] = datetime.now().timestamp() - starttime
        report['starttime'] = int(starttime)
        report['success'] = success

        # get repo details
        if repo_details is True and success is True:
            report['repo'] = infos_from_jar(file=fp, fingerprint=fingerprint)

        # delete temporary file
        if success is True:
            os.unlink(fp.name)

        # get TLS version
        context = ssl.create_default_context()
        try:
            with socket.create_connection((hostname, 443), timeout=timeout) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    report['TLS'] = ssock.version()
        except Exception as e:
            print(e)
            report['errors']['TLS'] = str(e)

        # measuring TLS handshake latency
        p = subprocess.run(['./tlsping', '-json', hostname + ':443'],
                           capture_output=True,
                           text=True)
        if p.returncode == 0:
            report['tlsping'] = json.loads(p.stdout)
        else:
            report['errors']['tlsping'] = re.sub('^tlsping: ', '', p.stderr)

        # get ciphersuites
        p = subprocess.run(['nmap', '--script', 'ssl-enum-ciphers', '-p', '443', hostname],
                           capture_output=True,
                           text=True)
        if p.returncode != 0:
            report['errors']['tls_details'] = p.stderr
        else:
            accept_pat = re.compile(r'^\|')
            yaml_pat = re.compile(r'^\|[_ ]( *)(.*:)')
            convert_pat = re.compile(r'^\| ( *)([^:]+)$')
            text = ''
            syn_ack = True
            for line in p.stdout.split('\n'):
                if re.compile(r'^443/tcp filtered').match(line):
                    syn_ack = False
                    break

                if accept_pat.match(line):
                    line = yaml_pat.sub(r'\1\2', line)
                    line = convert_pat.sub(r'\1- "\2"', line)
                    text += line + '\n'
                    if line.find('|') != -1:
                        print('found | in line: ', line)
                        print(p.stdout)
                        exit(-1)
            if text:
                try:
                    data = yaml.safe_load(text)
                except Exception as e:
                    print(text)
                    print(e)

            err = False
            if data:
                try:
                    report['tls_details'] = data['ssl-enum-ciphers']
                except KeyError:
                    err = True
            else:
                err = True

            if err is True:
                if syn_ack is False:
                    print('No SYN ACK received')
                    report['errors']['tls_details'] = 'No SYN ACK received'
                else:
                    print(p.stdout)
                    report['errors']['tls_details'] = p.stdout

    return report
