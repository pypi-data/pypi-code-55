from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from airbornerf.netconfig.SchemaVersion import SchemaVersion
from airbornerf.netconfig.rf.AntennaPattern import AntennaPattern
from airbornerf.netconfig.rf.Carrier import Carrier
from airbornerf.netconfig.rf.Cell import Cell
