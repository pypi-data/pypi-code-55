#!/usr/bin/env python3

# stdlibs
from datetime import datetime, timezone
import json
import requests
import statistics


class History:
    '''
    History
    '''

    def __init__(self, url=None, timeout=60):
        self.url = url
        if url is not None:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            # convert timestamp string to int
            self.history = response.json(object_hook=lambda d: {int(k) if k.lstrip('-').isdigit() else k: v for k, v in d.items()})
        else:
            self.history = {}

    def save(self, path):
        '''
        Save history as JSON

        :param path: filepath
        '''
        with open(path, 'w') as fp:
            json.dump(self.history, fp)

    def add(self, status, timestamp):
        '''
        Append status to history

        :param status: dict
        :param timestamp: (int) save status in history under this timestamp
        '''
        if not isinstance(timestamp, int):
            raise TypeError('timestamp must be an integer')

        self.history[timestamp] = status

    def trim(self, hours):
        '''
        delete timestamps older than x hours

        :param hours: number of hours from now to the past
        :return: number of timestamps after trimming
        '''
        current_timestamp = int(datetime.now(timezone.utc).timestamp())
        border = current_timestamp - (60*60*hours)

        for timestamp in list(self.history.keys()):
            if int(timestamp) < border:
                del self.history[timestamp]

    def average_status(self, hours):
        '''
        calculate the average values of the last x hours and return as complete status dict

        :param hours: number of hours from now to the past
        :return: status dict
        '''

        latest_ts = 0
        relevant_ts = []
        current_ts = int(datetime.now(timezone.utc).timestamp())
        border = current_ts - (60*60*hours)

        for timestamp in list(self.history.keys()):
            ts = timestamp
            if ts >= border:
                # relevant
                relevant_ts.append(timestamp)

            if ts > latest_ts:
                latest_ts = ts

        status = self.history[latest_ts]

        # if there is just one timestamp skip calculations
        if len(relevant_ts) == 1:
            return status

        # check rate:
        # average_check_rate = len(relevant_ts) / hours

        for ts in relevant_ts:
            for mirror in self.history[ts]['mirrors']:
                # calculate average duration and standard deviation
                if mirror in status['mirrors']:
                    pass

        for mirror in status['mirrors']:
            url = mirror['url']
            durations = []
            errors = {}

            for ts in relevant_ts:
                for historical_mirror in self.history[ts]['mirrors']:
                    # calculate average duration and standard deviation
                    if historical_mirror['url'] == url:
                        if 'duration' in historical_mirror:
                            durations.append(historical_mirror['duration'])
                        else:
                            durations.append(0)

                        errors[ts] = historical_mirror['errors']

            median = statistics.median(durations)
            mean = statistics.fmean(durations)
            #  σ² / Var(duration)
            variance = statistics.pvariance(durations, mean)

            mirror['duration'] = mean
            mirror['duration_median'] = median
            mirror['duration_variance'] = variance

        return status
