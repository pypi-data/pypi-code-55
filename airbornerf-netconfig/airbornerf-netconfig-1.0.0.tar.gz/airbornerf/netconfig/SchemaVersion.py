from sqlalchemy import Column, Integer
from . import Base


class SchemaVersion(Base):
	__tablename__ = 'schema_version'
	id = Column(Integer, primary_key=True)
	version = Column(Integer, nullable=False)
