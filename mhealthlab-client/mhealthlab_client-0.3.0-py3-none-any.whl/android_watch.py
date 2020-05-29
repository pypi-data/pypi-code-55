import glob
import os
import datetime
import pandas as pd
import numpy as np
import progress.bar as progress
from loguru import logger


class AndroidWatch:

    ACTIGRAPH_TEMPLATE = """------------ Data File Created By ActiGraph GT3X+ ActiLife v6.13.3 Firmware v2.5.0 date format M/d/yyyy at {0} Hz  Filter Normal -----------
Serial Number: CLE2B2013XXXX
Start Time {1}
Start Date {2}
Epoch Period (hh:mm:ss) 00:00:00
Download Time {3}
Download Date {4}
Current Memory Address: 0
Current Battery Voltage: 4.21     Mode = 12
--------------------------------------------------
Accelerometer X,Accelerometer Y,Accelerometer Z"""

    ACTIGRAPH_FILENAME_TEMPLATE = "AndroidWatch ({})RAW.csv"
    ANNOTATION_FILENAME_TEMPLATE = "AndroidWatch.annotation.csv"

    def __init__(self, root_folder):
        self._root = root_folder

    def _parse_session(self):
        folders = glob.glob(os.path.join(self._root, "*", "*"), recursive=True)
        folders = list(filter(lambda path: os.path.isdir(path), folders))
        folders_as_ts = list(map(AndroidWatch.folder_name_to_date, folders))
        folders_as_ts = sorted(folders_as_ts)
        self._session_st = folders_as_ts[0]
        self._session_et = folders_as_ts[-1]
        return self._session_st, self._session_et

    def convert_to_actigraph(self, sr=50):
        self._parse_session()
        hourly_markers = pd.date_range(self._session_st, self._session_et,
                                       freq='1H').to_pydatetime().tolist()
        n = len(hourly_markers)
        bar = progress.ChargingBar(
            'Converting watch files to Actigraph csv', max=n, suffix='%(index)d/%(max)d (%(elapsed_td)s - %(eta_td)s)')
        file_date_str = pd.Timestamp(self._session_st).strftime('%Y-%m-%d')
        output_filepath = os.path.join(
            self._root, AndroidWatch.ACTIGRAPH_FILENAME_TEMPLATE.format(file_date_str))
        output_annotation_filepath = os.path.join(
            self._root, AndroidWatch.ANNOTATION_FILENAME_TEMPLATE)
        if os.path.exists(output_filepath):
            logger.info('Remove the existing watch Actigraph csv file')
            os.remove(output_filepath)
        if os.path.exists(output_annotation_filepath):
            logger.info(
                'Remove the existing watch missing data annotation file')
            os.remove(output_annotation_filepath)
        last_row = None
        for marker in hourly_markers:
            date_str = "{}-{:02d}-{:02d}".format(marker.year,
                                                 marker.month, marker.day)
            hour_str = "{:02d}-EDT".format(marker.hour)
            filepaths = glob.glob(os.path.join(
                self._root, date_str, hour_str, "*.sensor.csv"))
            if len(filepaths) == 0:
                filepath = None
            else:
                filepath = filepaths[0]
            hourly_df = self._regularize_samples(marker, filepath, sr)

            if hourly_df.iloc[0, :].isna().any() and last_row is not None:
                hourly_df.iloc[0, :] = last_row.values
                last_row = None
            if hourly_df.iloc[-1, :].notna().all():
                last_row = hourly_df.iloc[-1, :]
            hourly_df = hourly_df.iloc[:-1, :]
            annotation_df = self._data_to_annotation(hourly_df, sr=sr)
            self._save_as_actigraph(hourly_df, output_filepath, sr=sr)
            self._save_as_annotation(
                annotation_df, output_annotation_filepath)
            bar.next()
        bar.finish()
        logger.info(
            'Watch files are converted to Actigraph csv, stored at {}'.format(output_filepath))

    def _data_to_annotation(self, hourly_df, sr=50):
        test = hourly_df['X'].copy(deep=True)
        test.loc[test.notna()] = 0
        test = test.fillna(1)
        edges = test.diff()
        if test.iloc[0] == 0:
            edges[0] = 0
        else:
            edges[0] = 1
        sts = hourly_df.loc[edges == 1].index.tolist()
        ets = hourly_df.loc[edges == -1].index.tolist()
        if len(sts) > len(ets):
            ets += [hourly_df.index[-1]]

        out_df = pd.DataFrame(data={
            'HEADER_TIME_STAMP': sts,
            'START_TIME': sts,
            'STOP_TIME': ets,
            'LABEL_NAME': "Missing"
        }, index=range(len(sts)))
        return out_df

    def _save_as_annotation(self, out_df, output_filepath):
        if not os.path.exists(output_filepath):
            out_df.to_csv(output_filepath, mode='a', header=True, index=False)
        else:
            out_df.to_csv(output_filepath, mode='a', header=False, index=False)

    def _save_as_actigraph(self, out_df, output_filepath, sr=50):
        meta_sdate_str = '{dt.month}/{dt.day}/{dt.year}'.format(
            dt=self._session_st)
        meta_stime_str = self._session_st.strftime('%H:%M:%S')
        meta_edate_str = '{dt.month}/{dt.day}/{dt.year}'.format(
            dt=self._session_et)
        meta_etime_str = (self._session_et +
                          datetime.timedelta(hours=1)).strftime('%H:%M:%S')
        if not os.path.exists(output_filepath):
            # create
            with open(output_filepath, mode='w') as f:
                f.write(AndroidWatch.ACTIGRAPH_TEMPLATE.format(
                    sr, meta_stime_str, meta_sdate_str, meta_etime_str, meta_edate_str))
                f.write('\n')
        # append
        out_df.to_csv(output_filepath, mode='a', index=False,
                      header=False, float_format='%.6f')

    def _regularize_samples(self, start_time, filepath=None, sr=50):
        freq = str(int(1000 / sr)) + 'L'
        tolerance = str(int(500 / sr)) + 'L'
        sample_ts = pd.date_range(start_time, start_time +
                                  datetime.timedelta(hours=1), freq=freq)
        if filepath is None:
            out_df = sample_ts.to_frame(index=False)
            out_df.columns = ['HEADER_TIME_STAMP']
            out_df['X'] = np.nan
            out_df['Y'] = np.nan
            out_df['Z'] = np.nan
            out_df = out_df.set_index('HEADER_TIME_STAMP')
        else:
            input_data = pd.read_csv(
                filepath, header=0, index_col=None, infer_datetime_format=True, parse_dates=[0])
            input_data.columns = ['HEADER_TIME_STAMP', 'X', 'Y', 'Z']
            input_data = input_data.drop_duplicates(
                subset=['HEADER_TIME_STAMP'], keep='first')
            input_data = input_data.sort_values(by=['HEADER_TIME_STAMP'])
            input_data['HEADER_TIME_STAMP'] = input_data['HEADER_TIME_STAMP'] + \
                pd.Timedelta(1, unit='milliseconds')
            input_data = input_data.set_index('HEADER_TIME_STAMP')
            out_df = input_data.reindex(
                sample_ts, axis='index', method='nearest', tolerance=tolerance, limit=1)
            out_df.index.names = ['HEADER_TIME_STAMP']
        return out_df

    @staticmethod
    def folder_name_to_date(folder_name):
        hour = os.path.basename(folder_name).split('-')[0]
        date = os.path.basename(os.path.dirname(folder_name))
        date_parts = date.split('-')
        ts = datetime.datetime(int(date_parts[0]), int(date_parts[1]),
                               int(date_parts[2]), int(hour), 0, 0, 0)
        return ts


if __name__ == "__main__":
    watch = AndroidWatch('D:/datasets/sample_watch_data')
    watch.convert_to_actigraph(sr=50)
