#!/usr/bin/env python3

# internal:
from fdroid_mirror_monitor import collect, report, website
from fdroid_mirror_monitor.utils import parallelize, add_reports_to_history
# stdlibs
from datetime import datetime, timezone
import argparse
import json
import os


def main():
    parser = argparse.ArgumentParser(prog='fdroid_mirror_monitor', description='description blabla')
    parser.add_argument('--no_history',
                        help='''don't create history.json''',
                        action='store_true')
    parser.add_argument('--no_html',
                        help='''don't create htmls''',
                        action='store_true')
    parser.add_argument('--html',
                        help='create htmls from status.json file')
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
    args = parser.parse_args()

    output_dir = os.path.realpath(args.directory)

    if args.html:
        with open(output_dir + '/status.json', 'r') as fp:
            status = json.load(fp)
            website.create_html(report=status, dir=output_dir)
            exit(0)

    if args.mirrors:
        mirrors = args.mirrors.split(',')
    else:
        print("Collecting mirrors")
        mirrors = collect.mirrors()

    # TODO: create report with mirror URL instead of repo URL,
    # check for archive in create_report() instead of README
    repo_urls = []
    for mirror_url in mirrors:
        repo_urls.append(mirror_url + '/repo')

    if args.repos:
        repo_urls += collect.repos()

    timestamp = int(datetime.now(timezone.utc).timestamp())
    mirror_reports = []
    mirror_report_dict = parallelize(repo_urls, report.create, args.threads)
    for mirror in mirror_report_dict:
        mirror_reports.append(mirror_report_dict[mirror])

    status = dict()
    status['version'] = 1
    status['last_check'] = timestamp
    status['mirrors'] = mirror_reports

    # TODO: calculate some values from history and add to status
    os.makedirs(output_dir, exist_ok=True)
    with open(output_dir + '/status.json', 'w') as fp:
        json.dump(status, fp)

    if args.no_history is False:
        add_reports_to_history(status, timestamp, output_dir + '/history.json')

    if args.no_html is False:
        website.create_html(report=status, dir=output_dir)
