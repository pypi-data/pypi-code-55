#!/usr/bin/env python3
"""A tool for monitoring Internet connection speed."""

import json
import logging
import shlex
import shutil
import subprocess
import time
from collections import namedtuple
from collections.abc import Iterable
from datetime import timedelta

import bitmath
import click
from dateutil.parser import parse as parse_dt
from humanize import naturaldelta
from tabulate import tabulate

logger = logging.getLogger('net-speed-monitor')


class Threshold(click.ParamType):
    """A parameter type for speed result threshold definitions."""

    envvar_list_splitter = ' / '

    def convert(self, value, param, ctx):
        """Split the definitions into its component parts and coerce types."""
        fraction, sleep_duration, description = shlex.split(value)
        return float(fraction), timedelta(minutes=float(sleep_duration)), str(description)


@click.command(context_settings={'auto_envvar_prefix': 'SPEEDTEST'})
@click.option(
    '--speedtest-cmd', default='speedtest', show_default=True, metavar='COMMAND',
    help='The speedtest command to use.')
@click.option('-v', '--verbose', is_flag=True, help="Increase the log level to DEBUG.")
@click.option(
    '--result-file', type=click.File(), metavar='PATH',
    help='The path to a JSON file to load instead of running a speed test.')
@click.option(
    '-e', '--expected-bandwidth', type=lambda value: bitmath.Mb(float(value)), metavar='MBPS',
    help='The expected bandwidth in Mbps.')
@click.option(
    '-t', '--threshold', 'thresholds', type=Threshold(),
    default=(
        (0.6, 5, 'slow'),
        (0.3, 1, 'very slow'),
    ), show_default=True, metavar='FRACTION sleep_duration DESC', multiple=True,
    help='Add a threshold to control the retry logic. If using the env var `SPEEDTEST_THRESHOLDS`, '
         'separate definitions with " / " and quote descriptions that contain whitespace.')
@click.option(
    '--default-sleep', type=lambda mins: timedelta(minutes=float(mins)), default=60,
    show_default=True, metavar='MINS',
    help='The number of minutes to sleep if none of the thresholds are hit.')
@click.pass_context
def main(ctx, speedtest_cmd, verbose, result_file, expected_bandwidth, thresholds, default_sleep):
    """Monitor Internet connection speed."""
    logging.basicConfig(
        format='%(asctime)s [%(levelname)8s] %(name)s: %(message)s',
        level=logging.DEBUG if verbose else logging.INFO)

    log_table('Params:', sorted(ctx.params.items()))

    if result_file is None and shutil.which(speedtest_cmd) is None:
        raise click.ClickException(
            f'Command {speedtest_cmd!r} not found! Is Speedtest CLI installed? '
            'See https://www.speedtest.net/apps/cli')

    if result_file is not None:
        logger.info(f'Loading result from {result_file.name!r}')
        result = json.load(result_file, object_hook=parse_to_namedtuple)

    while True:
        if result_file is None:
            cmd = [speedtest_cmd, '--format=json']
            logger.info('Running speed test...')
            logger.debug(f'Executing {" ".join(cmd)!r}')
            output = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, text=True).stdout
            logger.debug(f'Output of speedtest command:\n{output}')
            result = json.loads(output, object_hook=parse_to_namedtuple)

        logger.debug(f'Raw result:\n{result}')
        log_table('Test results:', [
            ('Download speed', result.download.bandwidth.format("{value:.2f} {unit}ps")),
            ('Upload speed', result.upload.bandwidth.format("{value:.2f} {unit}ps")),
            ('Latency', f'{result.ping.latency:.1f} ms'),
            ('Jitter', f'{result.ping.jitter:.1f} ms'),
        ])

        if expected_bandwidth is None:
            sleep_duration = max(sleep_duration for _, sleep_duration, _ in thresholds)
            logger.info('Expected bandwidth unknown')
        else:
            thresholds = sorted(thresholds)
            log_table('Thresholds:', [
                (str(expected_bandwidth * fraction), desc, naturaldelta(sleep_duration))
                for fraction, sleep_duration, desc in thresholds
            ], ('Speed', 'Description', 'Sleep'))

            for fraction, sleep_duration, desc in thresholds:
                bandwidth_threshold = fraction * expected_bandwidth
                logger.debug(f'Checking: {result.download.bandwidth} < {bandwidth_threshold}')
                if result.download.bandwidth < bandwidth_threshold:
                    logger.warning(f'Download speed is {desc}')
                    break
            else:
                logger.info('Download speed OK')
                sleep_duration = default_sleep

        if result_file is not None:
            logger.info(f'Would sleep for {naturaldelta(sleep_duration)}')
            logger.info('Not actually sleeping or retrying as result file provided')
            break

        sleep_delta(sleep_duration)


def parse_to_namedtuple(obj):
    """Parse a JSON object into a namedtuple.

    This is designed to be used as an "object hook" for `json.load` and friends.
    """
    type_ = namedtuple('_', obj.keys())
    values = []
    for key, value in obj.items():
        if key in {'bandwidth', 'bytes'}:
            values.append(bitmath.Mb(bytes=value))
        elif key in {'timestamp'}:
            values.append(parse_dt(value))
        else:
            values.append(value)

    return type_(*values)


def log_table(preamble: str, data: Iterable, headers=(), log_level=logging.DEBUG):
    """Log tabular data."""
    table = tabulate(data, headers, tablefmt='plain')
    logger.log(log_level, preamble)
    for line in table.splitlines():
        logger.log(log_level, f'  {line}')


def sleep_delta(delta: timedelta):
    """Sleep for a duration defined by a delta."""
    logger.info(f'Sleeping for {naturaldelta(delta)}...')
    time.sleep(delta.total_seconds())


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
