from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    UniqueConstraint,
    ForeignKey,
)

from ...database import Base


class SetIDPharmacologicCrossModel(Base):
    __tablename__ = "set_id_pharmacologic"

    spl_set_id = Column(String(128), required=True, primary_key=True)
    pharma_set_id = Column(String(128), required=True, index=True)
