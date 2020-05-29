import math
import pandas as pd
import pickle as pkl
from ..wrapper.mysql import DerivedDatabaseConnector
from ..view.derived_models import *

class DerivedDataApi(object):
    def get_fund_indicator(self, fund_list):
        with DerivedDatabaseConnector().managed_session() as quant_session:
            try:
                query = quant_session.query(
                        FundIndicator.fund_id,
                        FundIndicator.datetime,
                        FundIndicator.alpha,
                        FundIndicator.beta,
                        FundIndicator.fee_rate,
                        FundIndicator.track_err,
                    ).filter(
                        FundIndicator.fund_id.in_(fund_list),
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df
            
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))
        
    def get_fund_score(self):
        with DerivedDatabaseConnector().managed_session() as quant_session:
            try:
                query = quant_session.query(
                        FundScore,   
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df
            
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_index_valuation(self, index_id, start_date):
        with DerivedDatabaseConnector().managed_session() as mn_session:
            try:
                query = mn_session.query(
                    IndexValuation
                ).filter(
                    IndexValuation.index_id == index_id,
                    IndexValuation.datetime >= start_date,
                ).order_by(IndexValuation.datetime.asc())
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print(e)
                return pd.DataFrame([])

    def get_index_valuation_develop(self, index_ids, start_date, end_date):
        with DerivedDatabaseConnector().managed_session() as mn_session:
            try:
                query = mn_session.query(
                    IndexValuationDevelop
                ).filter(
                    IndexValuationDevelop.index_id.in_(index_ids),
                    IndexValuationDevelop.datetime >= start_date,
                    IndexValuationDevelop.datetime <= end_date,
                ).order_by(IndexValuationDevelop.datetime.asc())
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print(e)
                return pd.DataFrame([])

    def get_index_valuation_develop_without_date(self, index_ids):
        with DerivedDatabaseConnector().managed_session() as mn_session:
            try:
                query = mn_session.query(
                    IndexValuationDevelop
                ).filter(
                    IndexValuationDevelop.index_id.in_(index_ids),
                ).order_by(IndexValuationDevelop.datetime.asc())
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print(e)
                return pd.DataFrame([])

    def get_asset_allocation_info(self, version:int=2):
        with DerivedDatabaseConnector().managed_session() as mn_session:
            try:
                query = mn_session.query(
                    AssetAllocationInfo
                ).filter(
                    AssetAllocationInfo.version == version
                ).order_by(AssetAllocationInfo.allocation_id)
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print(e)
                return pd.DataFrame([])