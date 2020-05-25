#!/usr/bin/env python3

# internal:
from fdroid_mirror_monitor import collect, history, report, website
from fdroid_mirror_monitor.utils import parallelize, get_logger, geoip, own_ip
# stdlibs
from datetime import datetime, timezone
from importlib.metadata import metadata
from os import makedirs, path
import argparse
import json


def main():
    parser = argparse.ArgumentParser(prog='fdroid_mirror_monitor', description=metadata(__package__)['Summary'])
    parser.add_argument('--no_history',
                        help='''don't create history.json''',
                        action='store_true')
    parser.add_argument('--no_html',
                        help='''don't create htmls''',
                        action='store_true')
    parser.add_argument('--html',
                        help='create htmls from status.json file')
    parser.add_argument('--history_url',
                        help='URL to the the history in JSON format',
                        default='https://marzzzello.gitlab.io/mirror-monitor/history.json')
    parser.add_argument('-d', '--directory',
                        help='output directory',
                        default='public')
    parser.add_argument('-m', '--mirrors',
                        help='Comma seperated list of mirrors to check')
    parser.add_argument('-r', '--repos',
                        help='Extract repos from izzy, wiki',
                        action='store_true')
    parser.add_argument('-t', '--threads',
                        help='Number of parallel threads when checking mirrors',
                        choices=range(1, 10), type=int,
                        default=5)
    parser.add_argument('--trim',
                        help='Trim history entries to the last x hours',
                        type=int,
                        default=24*7)
    parser.add_argument('-v', '--verbosity',
                        help='Set verbosity level',
                        choices=['warning', 'info', 'debug'],
                        default='info')
    args = parser.parse_args()

    output_dir = path.realpath(args.directory)

    # init logger
    log = get_logger(__name__, args.verbosity)

    if args.html:
        with open(output_dir + '/status.json', 'r') as fp:
            status = json.load(fp)
            website.create_html(report=status, dir=output_dir)
            exit(0)

    if args.mirrors:
        mirrors = args.mirrors.split(',')
    else:
        log.info('Collecting mirrors')
        mirrors = collect.mirrors()

    # TODO: create report with mirror URL instead of repo URL,
    # check for archive in create_report() instead of README
    repo_urls = []
    for mirror_url in mirrors:
        repo_urls.append(mirror_url + '/repo')

    if args.repos:
        log.info('Collecting repos')
        repo_urls += collect.repos()

    timestamp = int(datetime.now(timezone.utc).timestamp())
    mirror_reports = []
    mirror_report_dict = parallelize(repo_urls, report.create, args.threads)
    for mirror in mirror_report_dict:
        mirror_reports.append(mirror_report_dict[mirror])

    status = dict()
    status['version'] = metadata(__package__)['Version']
    status['last_check'] = timestamp
    status['check_ip'] = own_ip()
    status['check_country'], status['check_country_code'] = geoip(status['check_ip'])
    status['mirrors'] = mirror_reports

    makedirs(output_dir, exist_ok=True)

    if args.no_history is False:
        log.info('Adding report to history')
        try:
            h = history.History(args.history_url)
            log.debug('The history had %s entries', len(h.history))
        except Exception as e:
            log.warning(str(e))
            log.error('Could not fetch history from %s', args.history_url)
            log.info('Creating empty history')
            h = history.History()

        h.add(status, timestamp)
        h.trim(args.trim)

        if len(h.history) == 1:
            log.debug('After trimming to the last %s hours the history has %s entry', args.trim, len(h.history))
        else:
            log.debug('After trimming to the last %s hours the history has %s entries', args.trim, len(h.history))

        h.save(path.join(args.directory, 'history.json'))
        status = h.average_status(args.trim)

    with open(path.join(output_dir, 'status.json'), 'w') as fp:
        json.dump(status, fp)

    if args.no_html is False:
        log.info('Creating HTMLs')
        website.create_html(report=status, dir=output_dir)
