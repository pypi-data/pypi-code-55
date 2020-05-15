from sqlalchemy import Column, String, Integer, Float, CheckConstraint
from sqlalchemy.orm import relationship
from .. import Base

class Carrier(Base):
	__tablename__ = 'carrier'
	__table_args__ = (
		CheckConstraint('technology = \'4G\' OR technology = \'5G\''),
		CheckConstraint('bandwidth >= 1000000 AND bandwidth <= 20000000'),
		CheckConstraint('frequency_band >= 1 AND frequency_band <= 100'),
	)
	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	technology = Column(String, nullable=False)
	bandwidth = Column(Integer, nullable=False)
	frequencyBand = Column(Integer, nullable=False, name='frequency_band')
	dlLowerFrequency = Column(Float, nullable=False, name='dl_lower_frequency')
	ulLowerFrequency = Column(Float, nullable=False, name='ul_lower_frequency')
	cell = relationship('Cell', uselist=False, back_populates='carrier')