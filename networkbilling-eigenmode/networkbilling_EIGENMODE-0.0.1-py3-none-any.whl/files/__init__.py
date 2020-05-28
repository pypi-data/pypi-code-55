
import networkbilling.files.bill as bill
import networkbilling.files.dispute as dispute
import networkbilling.files.outstanding as outstanding
import networkbilling.files.balance as balance
import networkbilling.files.remittance as remittance

from typing import Any, Type


# can throw ValueError due to date parsing

import csv
import io
import pathlib as pl


def from_filesystem(path: pl.Path) -> Type[object]:
    with open(path, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
        header_record_type = int(data[0][0])
        return header_mapping(header_record_type)(data)


def from_str(f: str) -> Type[object]:
    reader = csv.reader(io.StringIO(f))
    data = list(reader)
    header_record_type = int(data[0][0])
    return header_mapping(header_record_type)(data)

def header_mapping(record_type: int) -> Any:
    to_fn = {
        10: bill.Bill,
        800: remittance.Remittance,
        913: dispute.Dispute,
        930: outstanding.Outstanding,
        940: balance.Balance,
    }
    return to_fn[record_type]
