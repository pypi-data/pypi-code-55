from collections import defaultdict
from datetime import datetime

from .items import get_collection, get_item, parse_data
from .models import Settings
from .sheet_transform import get_col_item_needs, get_no_hide_collections, get_rows


def get_important(rows):
    imp_items = defaultdict(set)

    for col_name, items in get_col_item_needs(rows).items():
        for item_name in items:
            of_import = not item_name.startswith('!')
            item_name = item_name.strip('!')
            item = get_item(item_name, col_name)
            print(f'{col_name:>30} - {item_name:>30} --> {item.name}')
            imp_items[of_import].add(item)

    return imp_items[True], imp_items[False]


def remove_no_hide_cols(unimportant, rows):
    no_hide_col_names = get_no_hide_collections(rows)
    no_hide_cols = [get_collection(name) for name in no_hide_col_names]

    return {it for it in unimportant if it.collection not in no_hide_cols}


def get_settings():
    _, items = parse_data()
    rows = get_rows()

    important, unimportant = get_important(rows)

    unimportant |= items - important

    unimportant = remove_no_hide_cols(unimportant, rows)

    return Settings(important_items=important, unimportant_items=unimportant)


def write_export(export_path):
    now = datetime.now()
    path = export_path / now.strftime('%Y-%m-%d_%H-%M-%S.json')

    s = get_settings()
    path.write_text(s.as_json())

    print(f'export written to {path}')
