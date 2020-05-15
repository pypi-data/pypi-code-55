#!/usr/bin/env python3


import asyncio

import asyncpg
# IMPORTANT: ON OSX SHAPELY NEEDS TO BE IMPORTED BEFORE FIONA TO AVOID A CRASH IN GEOS LIBRARY
from shapely import geometry
import fiona

import gv_services.storage.dbstorage.dbrequest as dbrequest
from gv_services.storage.dbstorage import settings
from gv_utils import datetime, enums


ATT = enums.AttId.att
DATAPOINTEID = enums.AttId.datapointeid
DATATYPEEID = enums.AttId.datatypeeid
EID = enums.AttId.eid
FOW = enums.AttId.fow
FRC = enums.AttId.frc
FROMNO = enums.AttId.fromno
GEOM = enums.AttId.geom
ID = enums.AttId.id
LENGTH = enums.AttId.length
MAXSPEED = enums.AttId.maxspeed
NAME = enums.AttId.name
NLANES = enums.AttId.nlanes
NO = enums.AttId.no
ROADEID = enums.AttId.roadeid
TONO = enums.AttId.tono
VALIDFROM = enums.AttId.validfrom
WEBATT = enums.AttId.webatt

METROPMEDATATYPE = enums.DataTypeId.metropme
TOMTOMFCDDATATYPE = enums.DataTypeId.tomtomfcd
ROADSDATATYPE = enums.DataTypeId.roads


class DbStorage:

    def __init__(self, *credentials):
        self.host, self.port, self.database, self.user, self.password = credentials
        self.dbpool = None
        self.datatypeseidtoid = {}
        self.datapointseidtoid = {}
        self.roadseidtoid = {}

    async def async_init(self):
        self.dbpool = await asyncpg.create_pool(host=self.host, port=self.port, database=self.database,
                                                user=self.user, password=self.password)
        await self._init_cache()

    async def import_shapefile(self, shapefilepath):
        def get_roads():
            roads = []
            with fiona.open(shapefilepath, 'r', encoding='utf8') as features:
                for feature in features:
                    properties = feature['properties']
                    roads.append({
                        ATT: {
                            FOW: int(properties[FOW]),
                            FROMNO: int(properties[FROMNO]),
                            LENGTH: int(properties[LENGTH]),
                            NLANES: int(properties[NLANES]),
                            NO: int(properties[NO]),
                            TONO: int(properties[TONO])
                        },
                        EID: str(properties[EID]),
                        GEOM: geometry.shape(feature['geometry']),
                        WEBATT: {
                            FRC: int(properties[FRC]),
                            MAXSPEED: int(properties[MAXSPEED]),
                            NAME: str(properties[NAME])
                        }
                    })
            return roads
        await self.insert_roads(await asyncio.get_event_loop().run_in_executor(None, get_roads))

    async def insert_data_points(self, datapoints):
        if isinstance(datapoints, dict):
            datapoints = [datapoints, ]

        inserteddatapoints = list()
        for datapoint in datapoints:
            datatypeeid = datapoint[DATATYPEEID]
            if datatypeeid not in self.datatypeseidtoid:
                self._add_data_type_to_cache(await dbrequest.insert_data_type(self.dbpool, datatypeeid))
            if datapoint[EID] not in self.datapointseidtoid:
                inserteddatapoints.append((None, datapoint[EID], self.datatypeseidtoid[datatypeeid], datapoint[GEOM]))

        async for dpideid in await dbrequest.insert_data_points(self.dbpool, inserteddatapoints):
                self._add_data_point_to_cache(dpideid)
        return datapoints

    async def insert_roads(self, roads):
        if isinstance(roads, dict):
            roads = [roads, ]

        insertedroads = list()
        for road in roads:
            if road[EID] not in self.roadseidtoid:
                insertedroads.append((None, road[EID], road[ATT], road[WEBATT], road[GEOM]))

        async for rideid in await dbrequest.insert_roads(self.dbpool, insertedroads):
            self._add_road_to_cache(rideid)
        return roads

    async def insert_roads_data_points(self, roaddatapoints):
        if isinstance(roaddatapoints, dict):
            roaddatapoints = [roaddatapoints, ]

        validfrom = datetime.now(True)
        insertedroadsdatapoints = list()
        for roaddatapoint in roaddatapoints:
            reid = roaddatapoint[ROADEID]
            dpeid = roaddatapoint[DATAPOINTEID]
            if reid in self.roadseidtoid and dpeid in self.datapointseidtoid:
                insertedroadsdatapoints.append((self.roadseidtoid[reid], self.datapointseidtoid[dpeid],
                                                roaddatapoint.get(VALIDFROM, validfrom)))

        await dbrequest.insert_roads_data_points(self.dbpool, insertedroadsdatapoints)
        return roaddatapoints

    async def insert_traffic_data(self, samples, datatypeeid, timestamp):
        success = False
        if datatypeeid == METROPMEDATATYPE or datatypeeid == TOMTOMFCDDATATYPE:
            success = await self._insert_traffic_indicators(samples, timestamp, self.datapointseidtoid,
                                                            settings.DATA_POINTS_INDICATORS,
                                                            dbrequest.insert_data_points_indicators)
        elif datatypeeid == ROADSDATATYPE:
            success = await self._insert_traffic_indicators(samples, timestamp, self.roadseidtoid,
                                                            settings.ROADS_INDICATORS,
                                                            dbrequest.insert_roads_indicators)
        return success

    async def update_network_data_quality(self, dataquality, datatypeeid, freq=1):
        if datatypeeid not in self.datatypeseidtoid:
            return
        await dbrequest.update_network_data_quality(self.dbpool, dataquality, self.datatypeseidtoid[datatypeeid], freq)

    async def update_roads_ffspeeds(self, eidsffspeeds):
        await dbrequest.update_roads_ffspeeds(self.dbpool, eidsffspeeds)

    async def get_data_points(self, eids=None, datatypeeids=None, area=None):
        return await dbrequest.select_data_points(self.dbpool, eids, datatypeeids, area)

    async def get_roads(self, eids=None, area=None, hasmapping=False):
        return await dbrequest.select_roads(self.dbpool, eids, area, hasmapping)

    async def get_mapping_roads_data_points(self, roadeids=None, dpeids=None, validat=None):
        return await dbrequest.select_roads_data_points_eids(self.dbpool, roadeids, dpeids, validat)

    async def get_data_eids(self, datatypeeid, fromdate, todate, area=None):
        trafficieids = ''

        if datatypeeid == METROPMEDATATYPE or datatypeeid == TOMTOMFCDDATATYPE:
            trafficieids = await self._get_data_points_indicators_eids(datatypeeid, fromdate, todate, area)
        elif datatypeeid == ROADSDATATYPE:
            trafficieids = await self._get_roads_indicators_eids(fromdate, todate, area)

        return trafficieids

    async def get_data_quality(self, datatypeeid):
        result = {}
        if datatypeeid in self.datatypeseidtoid:
            result = await dbrequest.select_network_data_quality(self.dbpool, self.datatypeseidtoid[datatypeeid])
        return result

    async def _init_cache(self):
        self.datatypeseidtoid = {}
        self.datapointseidtoid = {}
        self.roadseidtoid = {}
        await asyncio.gather(self._init_data_types_cache(), self._init_data_points_cache(), self._init_roads_cache())

    async def _init_data_types_cache(self):
        result = await dbrequest.select_data_types_ids(self.dbpool)
        if result:
            self.datatypeseidtoid = result

    async def _init_data_points_cache(self):
        result = await dbrequest.select_data_points_ids(self.dbpool)
        if result:
            self.datapointseidtoid = result

    async def _init_roads_cache(self):
        result = await dbrequest.select_roads_ids(self.dbpool)
        if result:
            self.roadseidtoid = result

    def _add_data_type_to_cache(self, datatype):
        self.datatypeseidtoid[datatype[EID]] = datatype[ID]

    def _add_data_point_to_cache(self, datapoint):
        self.datapointseidtoid[datapoint[EID]] = datapoint[ID]

    def _add_road_to_cache(self, road):
        self.roadseidtoid[road[EID]] = road[ID]

    async def _insert_traffic_indicators(self, samples, timestamp, eidtoid, indicatorsid, insert_coro):
        rows = []
        for eid, sample in samples.items():
            locid = eidtoid.get(eid)
            if locid is None:
                continue
            row = [locid, timestamp]
            for indicator in indicatorsid:
                row.append(sample.get(indicator))
            rows.append(row)
        await insert_coro(self.dbpool, rows)
        return True

    async def _get_data_points_indicators_eids(self, datatypeeid, fromdate, todate, area):
        if datatypeeid not in self.datatypeseidtoid:
            return ''

        return await dbrequest.select_data_points_indicators_eids(self.dbpool, self.datatypeseidtoid[datatypeeid],
                                                                  fromdate, todate, area)

    async def _get_roads_indicators_eids(self, fromdate, todate, area):
        return await dbrequest.select_roads_indicators_eids(self.dbpool, fromdate, todate, area)

    def __del__(self):
        try:
            self.dbpool.terminate()
        except:
            pass
