from sqlalchemy import Column, String, Integer, Float, LargeBinary, CheckConstraint
from airbornerf.netconfig.types.UUID import UUID
from sqlalchemy.orm import relationship
from .. import Base
import uuid


class AntennaPattern(Base):
	__tablename__ = 'antenna_pattern'
	id = Column(UUID, default=uuid.uuid4, primary_key=True)
	eDownTilt = Column(Integer, nullable=False, name="e_down_tilt")
	gain = Column(Float, nullable=False)
	horizontalPattern = Column(LargeBinary, nullable=False, name='horizontal_pattern')
	verticalPattern = Column(LargeBinary, nullable=False, name='vertical_pattern')
	cell = relationship('Cell', uselist=False, back_populates='antennaPattern')
	upstreamName = Column(String, name='upstream_name')
	upstreamId = Column(String, name='upstream_id')
	polarization = Column(String, nullable=False, name='polarization')

	def dump(self):
		print(self.__dict__)

