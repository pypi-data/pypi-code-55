"""
Specific helpers to work with my RDR2 collecting spreadsheet data.
"""
from .gsheets import get_sheet_rows


ITEM_ROWS = 9


def get_rows(spreadsheet_name='RDR2 Collecting Needs', sheet_name="Tom"):
    return get_sheet_rows(spreadsheet_name, sheet_name)


def get_col_item_needs(rows):
    data = {}
    for prefix, col_name, *items in zip(*rows[: 2 + ITEM_ROWS]):
        if prefix and col_name != 'Weekly':
            col_name = f'{prefix} - {col_name}'
        data[col_name] = [it for it in items if it]

    return data


def get_no_hide_collections(rows):
    cols = set()
    no_hide_rows = [row for row in rows if row[0] == 'No hide']
    rows = rows[:2] + no_hide_rows
    for prefix, col_name, no_hide in zip(*rows):
        if prefix and col_name != 'Weekly':
            col_name = f'{prefix} - {col_name}'
        if no_hide:
            cols.add(col_name)

    return cols


if __name__ == '__main__':
    rows = get_rows()
    print(rows)
    print()

    col_item_needs = get_col_item_needs(rows)
    print(col_item_needs)
