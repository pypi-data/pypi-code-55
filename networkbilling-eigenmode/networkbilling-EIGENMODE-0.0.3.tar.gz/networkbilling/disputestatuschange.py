from typing import List, Iterable, Optional
import dateutil.parser as du
import datetime as dt

from pydantic.dataclasses import dataclass
from pydantic import constr, condecimal

import networkbilling.base as base

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
        return 913

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
    line_id: constr(max_length=17)

    nmi: constr(max_length=10)
    nmi_checksum: constr(min_length=1, max_length=1)

    new_status_code: constr(max_length=4)
    status_change_comments: Optional[constr(max_length=240)]

    @staticmethod
    def record_type() -> int:
        return 914

    @staticmethod
    def from_row(row: List[str]) -> "Detail":
        return Detail(
            unique_number=row[1],
            line_id=row[2],
            nmi=row[3],
            nmi_checksum=row[4],
            new_status_code=row[5],
            status_change_comments=row[6]
        )


@dataclass(frozen=True)
class Footer(base.FooterRow):
    record_count: condecimal(max_digits=10, decimal_places=0)

    @staticmethod
    def record_type() -> int:
        return 915

    @staticmethod
    def from_row(row: List[str]) -> "Footer":
        return Footer(
            record_count=row[1],
        )


class DisputeStatusChange:
    header: Header
    footer: Footer
    details: List[Detail] = list()

    @staticmethod
    def from_filesystem(path: pl.Path) -> "DisputeStatusChange":
        with open(path, 'r') as f:
            return DisputeStatusChange(csv.reader(f))

    @staticmethod
    def from_str(f: str) -> "DisputeStatusChange":
        return DisputeStatusChange(csv.reader(io.StringIO(f)))

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
                    "got {got} when parsing dispute file row {row}"
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
