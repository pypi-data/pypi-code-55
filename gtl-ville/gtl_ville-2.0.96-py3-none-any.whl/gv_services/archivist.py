#!/usr/bin/env python3

import asyncio
import traceback

from gv_services.proto.archivist_pb2 import TrafficData
from gv_services.storage import filestorage
from gv_utils import datetime, enums, geometry, protobuf
from gv_utils import csv

CONFIDENCE = enums.CsvData.confidence
FLOW = enums.CsvData.flow
SAMPLES = enums.CsvData.samples

METROPME = enums.DataTypeId.metropme
TOMTOMFCD = enums.DataTypeId.tomtomfcd
ROADS = enums.DataTypeId.roads
ZONES = enums.DataTypeId.zones


class Archivist:

    def __init__(self, logger, basedatapath, dbstorage):
        super().__init__()
        self.logger = logger
        self.basedatapath = basedatapath
        self.dbstorage = dbstorage

    async def store_data(self, pbtrafficdata, datatype, pbtimestamp):
        success = False
        try:
            trafficsamples = (await protobuf.decode_traffic_data(pbtrafficdata))[SAMPLES]
            timestamp = datetime.from_timestamp(pbtimestamp.ToSeconds())
            coros = [
                filestorage.write_data(self.basedatapath, pbtrafficdata.trafficdata, datatype, timestamp),
                self.dbstorage.insert_traffic_data(trafficsamples, datatype, timestamp)
            ]
            if 6 <= timestamp.hour <= 19:
                coros.append(self._store_data_quality(trafficsamples, datatype))
            status = await asyncio.gather(*coros)
            success = bool(int(sum(status) / len(status)))
            self.logger.debug('Archivist stored {} data.'.format(datatype))
        except:
            self.logger.error(traceback.format_exc())
            self.logger.error('An error occurred while storing {} data.'.format(datatype))
        finally:
            return success

    async def _store_data_quality(self, trafficsamples, datatype):
        success = False
        try:
            dataquality = None
            freq = 1
            if datatype == METROPME:
                dataquality = self._compute_metropme_quality(trafficsamples)
            elif datatype == TOMTOMFCD or datatype == ROADS:
                dataquality = self._compute_tomtomfcd_quality(trafficsamples)
            if dataquality is not None:
                await self.dbstorage.update_network_data_quality(dataquality, datatype, freq)
                success = True
        except:
            self.logger.error(traceback.format_exc())
            self.logger.error('An error occurred while storing {} data quality.'.format(datatype))
        finally:
            return success

    @staticmethod
    def _compute_metropme_quality(data):
        ntotal = len(data)
        nvalid = 0
        for sample in data.values():
            if sample.get(FLOW, -1) >= 0:
                nvalid += 1
        return int(100 * nvalid / ntotal)

    @staticmethod
    def _compute_tomtomfcd_quality(data):
        confidences = []
        for sample in data.values():
            confidence = sample.get(CONFIDENCE, -1)
            if confidence >= 0:
                confidences.append(confidence)
        return int(sum(confidences) / max(len(confidences), 1))

    async def get_data(self, request):
        datatype = request.datatype
        fromdate, todate = datetime.from_timestamp(request.fromdate.ToSeconds()), \
                           datetime.from_timestamp(request.todate.ToSeconds())
        freq = request.freq
        noeids = request.noeids
        area = request.area
        window = request.window
        if freq < 1:
            freq = 1
        try:
            area = geometry.decode_geometry(area)
        except:
            area = None

        try:
            if datatype not in (METROPME, TOMTOMFCD, ROADS, ZONES):
                raise ValueError('Unknown data type')

            if noeids or area is not None:
                trafficeids = ''
                try:
                    trafficeids = await self.dbstorage.get_data_eids(datatype, fromdate, todate, area)
                except:
                    self.logger.error(traceback.format_exc())
                    self.logger.error('An error occurred while getting {} eids between {} and {}.'
                                      .format(datatype, datetime.to_string(fromdate), datetime.to_string(todate)))
                finally:
                    yield TrafficData(trafficdata=trafficeids.encode(csv.ENCODING), applyto='header')

            for startday, endday in datetime.split_in_days(fromdate, todate):
                try:
                    async for data in filestorage.get_data(datatype, startday, endday, self.basedatapath, freq, window):
                        yield TrafficData(trafficdata=data, applyto='minute')
                        self.logger.debug('Archivist served {} data.'.format(datatype))
                except:
                    self.logger.error(traceback.format_exc())
                    self.logger.error('An error occurred while getting {} data for day {}.'
                                      .format(datatype, startday))
                    yield TrafficData(trafficdata=b'', applyto='day')
        except:
            self.logger.error(traceback.format_exc())
            self.logger.error('An error occurred while getting {} data between {} and {}.'
                              .format(datatype, datetime.to_string(fromdate), datetime.to_string(todate)))
            yield TrafficData(trafficdata=b'', applyto='all')

    async def get_data_quality(self, request):
        datatype = request.datatype
        dataquality = b''
        try:
            dataquality = await self.dbstorage.get_data_quality(datatype)
        except:
            self.logger.error(traceback.format_exc())
            self.logger.error('An error occurred while getting {} data quality.'.format(datatype))
        return await protobuf.encode_data_quality(dataquality)
