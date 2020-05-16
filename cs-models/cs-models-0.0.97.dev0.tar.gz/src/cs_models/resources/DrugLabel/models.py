from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    UniqueConstraint,
)

from datetime import datetime

from ...database import Base


class DrugLabelModel(Base):
    __tablename__ = 'drug_labels'

    id = Column(Integer, primary_key=True)
    spl_id = Column(String(128), nullable=False)
    set_id = Column(String(128), nullable=False)
    indication_text = Column(Text)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    __table_args__ = (
        UniqueConstraint(
            'spl_id',
            'set_id',
        ),
    )
