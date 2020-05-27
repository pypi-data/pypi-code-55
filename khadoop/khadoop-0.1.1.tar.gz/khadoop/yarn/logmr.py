"""parse raw log file produce in Yarn context
file look like: `hadoop-mapreduce.jobsummary.log`
"""
import logging

FILEPATTERN = 'hadoop-mapreduce.jobsummary.log*'


def is_application(line) -> bool:
    """use it to keep only relevant lines"""
    return ('name=oozie' not in line) and ('INFO resourcemanager.RMAppManager$ApplicationSummary' in line)


def parse_elt_meta(meta: str) -> dict:
    keys = ['day', 'time', 'level', 'javac']
    return {key: value for key, value in zip(keys, meta.split(' '))}


def parse_elt_payload(elts: str) -> dict:
    # note: a part of preemptedRessources is ignored
    # as it is splitted on two lines (filterd out by condition on '=')
    # ValueError
    try:
        return dict([tuple(elt.split('=')) for elt in elts.split(',') if '=' in elt])
    except ValueError:
        logging.error(elts)
        return {}


def parse_line(line: str) -> dict:
    meta, payload = line.split(': ')
    return {**parse_elt_meta(meta), **parse_elt_payload(payload)}
