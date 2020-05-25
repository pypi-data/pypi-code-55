from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List
from marshmallow import validate, validates_schema, ValidationError

from .enums import MeasurementType

@dataclass
class PublishMeasurementRequest:
    begin: datetime = field()   
    end: datetime = field()
    sector: str = field(metadata={"validate": validate.OneOf(['DK1', 'DK2'])})
    type: MeasurementType = field()
    amount: int = field(metadata={"validate": validate.Range(min=0)})

    @validates_schema
    def validate_dates(self, data, **kwargs):
        
        if  data['begin'] >= data['end']:
            raise ValidationError('Begin must be before End!')

        if (data['end'] - data['begin']) != timedelta(hours=1):
            raise ValidationError('Only positive hourly measurements are currently supported!')


@dataclass
class IssueGGORequest:
    origin: str = field()
    destination: str = field()
    tech_type: str = field()
    fuel_type: str = field()


@dataclass
class TransferGGORequest:
    origin: str = field()
    destination: str = field()
    

@dataclass
class SplitGGOPart:
    address: str = field()
    amount: int = field()


@dataclass
class SplitGGORequest:
    origin: str = field()
    parts: List[SplitGGOPart] = field()


@dataclass
class RetireGGORequest:
    origin: str = field()
    settlement_address: str = field()

    
@dataclass
class SettlementRequest:
    settlement_address: str = field()
    measurement_address: str = field()
    ggo_addresses: List[str] = field()
