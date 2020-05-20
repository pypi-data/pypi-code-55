# -*- coding: utf-8 -*-
from __future__ import with_statement, absolute_import, division
from KE.base import Base
import pandas as pd


class Query(Base):
    """The JSON returned by API V4 is different from V2"""
    def __init__(self, client=None, query_id=None):
        """Query Object
        """
        super(Query, self).__init__(client=client)
        self.id = query_id

    @classmethod
    def from_json(cls, client=None, json_obj=None):
        """Deserialize the job json object to a Job object

        :param client: the KE client
        :paramjson_obj: the job json object
        """
        query = Query(client=client, query_id=json_obj['queryId'])
        column_metas = json_obj['columnMetas']

        query.affectedRowCount = json_obj['affectedRowCount']
        query.isException = json_obj['isException']
        query.exceptionMessage = json_obj['exceptionMessage']
        query.duration = json_obj['duration']
        query.totalScanBytes = json_obj['totalScanBytes']
        query.hitExceptionCache = json_obj['hitExceptionCache']
        query.server = json_obj['server']
        query.timeout = json_obj['timeout']
        query.pushDown = json_obj['pushDown']
        query.results = json_obj['results']
        query.df = cls._to_pandas(query.results, column_metas)

        return query

    @staticmethod
    def _to_pandas(results, column_metas):
        if results:
            cols = [c['name'] for c in column_metas]
            df = pd.DataFrame(results, columns=cols)
            return df
        else:
            return pd.DataFrame()

    def __repr__(self):
        return '<Query %s>' % self.id
