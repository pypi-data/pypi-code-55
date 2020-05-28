from typing import List, Iterable, Dict
import dateutil.parser as du
import datetime as dt

from pydantic.dataclasses import dataclass
from pydantic import constr, condecimal

import networkbilling.files.base as base

import csv
import io
import pathlib as pl


@dataclass(frozen=True)
class Header(base.HeaderRow):
    dnsp_code: constr(max_length=10)
    retailer_code: constr(max_length=10)
    timestamp: str
    start_period: dt.date
    end_period: dt.date

    @staticmethod
    def record_type() -> int:
        return 930

    @staticmethod
    def from_row(row: List[str]) -> "Header":
        return Header(
            dnsp_code=row[1],
            retailer_code=row[2],
            # this is a workaround as some dnsp put the header
            # using scientific notation....
            timestamp=row[3],
            start_period=du.parse(row[4]).date(),
            end_period=du.parse(row[5]).date(),
        )


@dataclass(frozen=True)
class Detail(base.NetworkRow):
    unique_number: constr(max_length=20)

    nmi: constr(max_length=10)
    nmi_checksum: constr(min_length=1, max_length=1)

    issue_date: dt.date
    due_date: dt.date

    total_amount: condecimal(max_digits=15, decimal_places=2)

    dispute_recieved_indicator: constr(max_length=1)
    comments: constr(max_length=240)

    @staticmethod
    def record_type() -> int:
        return 931

    @staticmethod
    def from_row(row: List[str]) -> "Detail":
        return Detail(
            unique_number=row[1],
            nmi=row[2],
            nmi_checksum=row[3],
            issue_date=du.parse(row[4]).date(),
            due_date=du.parse(row[5]).date(),
            total_amount=row[6],
            dispute_recieved_indicator=row[7],
            comments=row[8],
        )


@dataclass(frozen=True)
class Footer(base.FooterRow):
    total_amount: condecimal(max_digits=15, decimal_places=2)
    record_count: condecimal(max_digits=10, decimal_places=0)

    @staticmethod
    def record_type() -> int:
        return 932

    @staticmethod
    def from_row(row: List[str]) -> "Footer":
        return Footer(
            record_count=row[1],
            total_amount=row[2],
        )


class Outstanding:
    header: Header
    footer: Footer
    details: List[Detail] = list()

    @staticmethod
    def from_filesystem(path: pl.Path) -> "Outstanding":
        with open(path, 'r') as f:
            return Outstanding(csv.reader(f))

    @staticmethod
    def from_str(f: str) -> "Outstanding":
        return Outstanding(csv.reader(io.StringIO(f)))

    def __init__(self, csv_reader: Iterable[List[str]]) -> None:
        rows = sum(1 for r in csv_reader)
        for row in csv_reader:
            record_type = int(row[0])
            if record_type == Header.record_type():
                self.header = Header.from_row(row)
            elif record_type == Footer.record_type():
                self.footer = Footer.from_row(row)
            elif record_type == Detail.record_type():
                self.details.append(Detail.from_row(row))
            else: 
                raise base.UnexpectedRecordType(
                    "got {got} when parsing Outstanding file row {row}"
                    .format(got=record_type, row=row))
        if self.header is None:
            raise base.MissingHeader()
        if self.footer is None:
            raise base.MissingFooter()
        if self.footer.record_count + 2 != rows:
            raise base.UnexpectedNumberOfRows(
                    "got {got} but expected {exp}"
                    .format(got=rows, exp=self.footer.record_count)
                    )
