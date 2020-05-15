from sqlalchemy import Column, String, Integer, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from airbornerf.netconfig.types.UUID import UUID
from .. import Base


class Cell(Base):
	__tablename__ = 'cell'
	__table_args__ = (
		CheckConstraint('latitude > -90 AND latitude < 90'),
		CheckConstraint('longitude > -180 AND longitude < 180'),
		CheckConstraint('azimuth >= 0 AND azimuth <= 359'),
		CheckConstraint('height >= 0'),
		CheckConstraint('technology = \'4G\' OR technology = \'5G\''),
		CheckConstraint('cell_load >= 0.0 AND cell_load <= 1.0'),
		CheckConstraint('pci >= 0 AND pci <= 503'),
		CheckConstraint('rs_dbm >= -60 AND rs_dbm <= 50'),
	)
	id = Column(Integer, primary_key=True)
	name = Column(String, name='name', nullable=False)
	CGI = Column(Integer, nullable=False, name='cgi')
	MCC = Column(Integer, nullable=False, name='mcc')
	MNC = Column(Integer, nullable=False, name='mnc')
	technology = Column(String, nullable=False)
	latitude = Column(Float, nullable=False)
	longitude = Column(Float, nullable=False)
	altitude = Column(Float, nullable=False)
	height = Column(Float, nullable=False)
	azimuth = Column(Integer, nullable=False)
	mDownTilt = Column(Integer, nullable=False, name="m_down_tilt")
	maxTXpower = Column(Float, nullable=False, name='max_tx_power')
	dlTXAntennae = Column(Integer, nullable=False, name='dl_tx_antennae')
	losses = Column(Float, nullable=False, name='losses')
	antennaPatternId = Column(UUID, ForeignKey('antenna_pattern.id'), nullable=False, name='antenna_pattern_id')
	antennaPattern = relationship('AntennaPattern', back_populates='cell')
	carrierId = Column(Integer, ForeignKey('carrier.id'), nullable=False, name='carrier_id')
	carrier = relationship('Carrier', back_populates='cell')
	PCI = Column(Integer, nullable=False, name='pci')
	cellLoad = Column(Float, nullable=False, name='cell_load')
	RSdBm = Column(Float, nullable=False, name="rs_dbm")
	offsetTraffic = Column(Float, nullable=False, name='offset_traffic', default=0)
	offsetBroadcast = Column(Float, nullable=False, name='offset_broadcast', default=0)
	offsetSynchronization = Column(Float, nullable=False, name='offset_synchronization', default=0)
	offsetControl = Column(Float, nullable=False, name='offset_control', default=0)

def dump(self):
		print(self.__dict__)

