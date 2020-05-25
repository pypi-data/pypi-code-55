# -*- coding: utf-8 -*-
__author__ = 'Gabriel Salgado'
__version__ = '0.5.1'

import pandas as pd


def filter_by_client(df: pd.DataFrame, client: str) -> pd.DataFrame:
	mask = df['contractName'] == client
	columns= ['dateEnd', 'MAUs', 'MEUs', 'MIUs']
	df_filtered = df.loc[mask, columns]
	df_filtered = df_filtered.reset_index(drop=True)
	return df_filtered


def format_dataframe(df: pd.DataFrame) -> pd.DataFrame:
	df_formatted = df.copy()
	df_formatted['dateEnd'] = df_formatted['dateEnd'].apply(pd.Timestamp)
	df_formatted = df_formatted.sort_values('dateEnd').set_index('dateEnd')
	return df_formatted


def limit_by_time(df: pd.DataFrame, t_init: str) -> pd.DataFrame:
	df_limited = df[t_init:]
	return df_limited


def transform_to_daily_new_users(df: pd.DataFrame) -> pd.DataFrame:
	df_diff = df.diff()[1:]
	df_diff[df_diff < 0] = df[df_diff < 0]
	df_diff = df_diff.rename(columns={'MAUs': 'New MAUs', 'MEUs': 'New MEUs', 'MIUs': 'New MIUs'})
	return df_diff
