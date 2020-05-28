from typing import List, Optional, Iterable, Dict
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

    @staticmethod
    def record_type() -> int:
        return 10

    @staticmethod
    def from_row(row: List[str]) -> "Header":
        return Header(
            dnsp_code=row[1],
            retailer_code=row[2],
            # this is a workaround as some dnsp put the header
            # using scientific notation....
            timestamp=row[3],
        )


@dataclass(frozen=True)
class Footer(base.FooterRow):
    charge_record_count: condecimal(max_digits=10, decimal_places=0)
    summary_record_count: condecimal(max_digits=10, decimal_places=0)
    total_tax_exclusive: condecimal(
            max_digits=15,
            decimal_places=2)
    total_tax_charge_payable: condecimal(
            max_digits=15,
            decimal_places=2)
    total_payable: condecimal(max_digits=15, decimal_places=2)

    @staticmethod
    def record_type() -> int:
        return 11

    @staticmethod
    def total_record_count(self) -> int:
        return int(self.charge_record_count) + int(self.summary_record_count)

    @staticmethod
    def from_row(row: List[str]) -> "Footer":
        return Footer(
            charge_record_count=row[1],
            summary_record_count=row[2],
            total_tax_exclusive=row[3],
            total_tax_charge_payable=row[4],
            total_payable=row[5],
        )


@dataclass(frozen=True)
class Summary(base.NetworkRow):
    unique_number: constr(max_length=20)
    nmi: constr(max_length=10)
    nmi_checksum: constr(min_length=1, max_length=1)
    issue_date: dt.date
    due_date: dt.date
    dnsp_name: constr(max_length=50)
    dnsp_abn: constr(max_length=14)
    retailer_name: constr(max_length=50)
    retailer_abn: constr(max_length=14)
    status: constr(max_length=20)
    tax_exclusive: condecimal(max_digits=15, decimal_places=2)
    tax_payable: condecimal(max_digits=15, decimal_places=2)
    amount_payable: condecimal(max_digits=15, decimal_places=2)
    tax_indicator: constr(min_length=1, max_length=1)

    @staticmethod
    def record_type() -> int:
        return 20

    @staticmethod
    def from_row(row: List[str]) -> "Summary":
        return Summary(
            unique_number=row[1],
            nmi=row[2],
            nmi_checksum=row[3],
            issue_date=du.parse(row[4]).date(),
            due_date=du.parse(row[5]).date(),
            dnsp_name=row[6],
            dnsp_abn=row[7],
            retailer_name=row[8],
            retailer_abn=row[9],
            status=row[10],
            tax_exclusive=row[11],
            tax_payable=row[12],
            amount_payable=row[13],
            tax_indicator=row[14],
        )


@dataclass(frozen=True)
class NuosCharge(base.NetworkRow):
    unique_number: constr(max_length=20)
    line_id: constr(max_length=17)
    old_unique_number: Optional[constr(max_length=20)]
    transaction_date: dt.date
    adjustment_indicator: constr(min_length=1, max_length=1)
    adjustment_reason: constr(max_length=60)
    nmi: constr(max_length=10)
    nmi_checksum: constr(min_length=1, max_length=1)
    tarrif_code: constr(max_length=10)
    step_number: condecimal(max_digits=3, decimal_places=0)
    start_date: dt.date
    end_date: dt.date
    tarrif_component_code: constr(max_length=10)
    reading_type: constr(min_length=1, max_length=1)
    line_description: constr(max_length=60)
    quantity: condecimal(max_digits=9, decimal_places=5)
    unit_of_measure: constr(max_length=5)
    rate: condecimal(max_digits=9, decimal_places=5)
    charge_amount: condecimal(max_digits=15, decimal_places=2)
    tax_charge_amount: condecimal(max_digits=15, decimal_places=2)
    tax_chage_indicator: constr(min_length=1, max_length=1)

    @staticmethod
    def record_type() -> int:
        return 100

    @staticmethod
    def from_row(row: List[str]) -> "NuosCharge":
        return NuosCharge(
            unique_number=row[1],
            line_id=row[2],
            old_unique_number=row[3],
            transaction_date=du.parse(row[4]).date(),
            adjustment_indicator=row[5],
            adjustment_reason=row[6],
            nmi=row[7],
            nmi_checksum=row[8],
            tarrif_code=row[9],
            step_number=row[10],
            start_date=du.parse(row[11]).date(),
            end_date=du.parse(row[12]).date(),
            tarrif_component_code=row[13],
            reading_type=row[14],
            line_description=row[15],
            quantity=row[16],
            unit_of_measure=row[17],
            rate=row[18],
            charge_amount=row[19],
            tax_charge_amount=row[20],
            tax_chage_indicator=row[21],
        )


@dataclass(frozen=True)
class EventCharge(base.NetworkRow):
    unique_number: constr(max_length=20)
    line_id: constr(max_length=17)
    old_unique_number: Optional[constr(max_length=20)]
    transaction_date: dt.date
    adjustment_indicator: constr(min_length=1, max_length=1)
    adjustment_reason: constr(max_length=60)
    nmi: constr(max_length=10)
    nmi_checksum: constr(min_length=1, max_length=1)

    network_service_order_ref: Optional[constr(max_length=15)]
    retailer_service_order_ref: Optional[constr(max_length=15)]
    network_rate_code: constr(max_length=10)

    line_description: constr(max_length=60)
    charge_date: dt.date
    quantity: condecimal(max_digits=5, decimal_places=0)
    unit_of_measure: constr(max_length=5)
    rate: condecimal(max_digits=9, decimal_places=5)
    charge_amount: condecimal(max_digits=15, decimal_places=2)
    tax_charge_amount: condecimal(max_digits=15, decimal_places=2)
    tax_chage_indicator: constr(min_length=1, max_length=1)

    @staticmethod
    def record_type() -> int:
        return 200

    @staticmethod
    def from_row(row: List[str]) -> "EventCharge":
        return EventCharge(
            unique_number=row[1],
            line_id=row[2],
            old_unique_number=row[3],
            transaction_date=du.parse(row[4]).date(),
            adjustment_indicator=row[5],
            adjustment_reason=row[6],
            nmi=row[7],
            nmi_checksum=row[8],
            network_service_order_ref=row[9],
            retailer_service_order_ref=row[10],
            network_rate_code=row[11],
            line_description=row[12],
            charge_date=du.parse(row[13]).date(),
            quantity=row[14],
            unit_of_measure=row[15],
            rate=row[16],
            charge_amount=row[17],
            tax_charge_amount=row[18],
            tax_chage_indicator=row[19],
        )


@dataclass(frozen=True)
class InterestCharge(base.NetworkRow):
    unique_number: constr(max_length=20)
    line_id: constr(max_length=17)
    old_unique_number: Optional[constr(max_length=20)]
    transaction_date: dt.date
    adjustment_indicator: constr(min_length=1, max_length=1)
    adjustment_reason: constr(max_length=60)
    nmi: constr(max_length=10)
    nmi_checksum: constr(min_length=1, max_length=1)

    overdue_statement_unique_number: constr(max_length=20)
    overdue_statement_due_date: dt.date
    principal_amount: condecimal(max_digits=15, decimal_places=2)
    interest_period_start_date: dt.date
    interest_period_end_date: dt.date

    interest_charge_amount: condecimal(max_digits=9, decimal_places=2)
    tax_charge_amount: condecimal(max_digits=9, decimal_places=2)
    tax_chage_indicator: constr(min_length=1, max_length=1)

    @staticmethod
    def record_type() -> int:
        return 900

    @staticmethod
    def from_row(row: List[str]) -> "InterestCharge":
        return InterestCharge(
            unique_number=row[1],
            line_id=row[2],
            old_unique_number=row[3],
            transaction_date=du.parse(row[4]).date(),
            adjustment_indicator=row[5],
            adjustment_reason=row[6],
            nmi=row[7],
            nmi_checksum=row[8],

            overdue_statement_unique_number=row[9],
            overdue_statement_due_date=du.parse(row[10]).date(),
            principal_amount=row[11],
            interest_period_start_date=du.parse(row[12]).date(),
            interest_period_end_date=du.parse(row[13]).date(),
            interest_charge_amount=row[14],
            tax_charge_amount=row[15],
            tax_chage_indicator=row[16],
        )


class Bill:
    header: Header
    footer: Footer
    summaries: List[Summary] = list()
    nuos: List[NuosCharge] = list()
    event: List[EventCharge] = list()
    interest: List[InterestCharge] = list()

    @staticmethod
    def from_filesystem(path: pl.Path) -> "Bill":
        with open(path, 'r') as f:
            return Bill(csv.reader(f))

    @staticmethod
    def from_str(f: str) -> "Bill":
        return Bill(csv.reader(io.StringIO(f)))

    def __init__(self, csv_reader: Iterable[List[str]]) -> None:
        rows = sum(1 for r in csv_reader)
        for row in csv_reader:
            record_type = int(row[0])
            if record_type == Header.record_type():
                self.header = Header.from_row(row)
            elif record_type == Footer.record_type():
                self.footer = Footer.from_row(row)
            elif record_type == Summary.record_type():
                self.summaries.append(Summary.from_row(row))
            elif record_type == NuosCharge.record_type():
                self.nuos.append(NuosCharge.from_row(row))
            elif record_type == EventCharge.record_type():
                self.event.append(EventCharge.from_row(row))
            elif record_type == InterestCharge.record_type():
                self.interest.append(InterestCharge.from_row(row))
            else:
                raise base.UnexpectedRecordType(
                    "got {got} when parsing bill file row {row}"
                    .format(got=record_type, row=row))
        if self.header is None:
            raise base.MissingHeader()
        if self.footer is None:
            raise base.MissingFooter()
        # have to include summary, charge, header and footer hance +2
        rc = self.footer.summary_record_count + self.footer.charge_record_count + 2
        if rc != rows:
            raise base.UnexpectedNumberOfRows(
                    "got {got} but expected {exp}"
                    .format(got=rows, exp=rc)
                    )
