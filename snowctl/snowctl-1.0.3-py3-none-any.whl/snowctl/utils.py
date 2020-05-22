import re
import os
import sys


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def format_ddl(ddl, view_name, target_schema, database):
    tokens = ddl.split()
    for i, token in enumerate(tokens):
        if token.lower() == 'view':
            tokens[i + 1] = f'{database}.{target_schema}.{view_name}'
            break
    new_ddl = ' '.join(tokens)
    return new_ddl


def filter_columns(cols: str, view, db, schema):
    r = []
    lst = cols.split(',')
    print()
    for i, col in enumerate(lst):
        print(f'{i} - {col}')
    print(f'\n{view}: target -> {db}.{schema}')
    print('choose columns NOT to include ([int, int, ...]): ', end='', flush=True)
    user_input = sys.stdin.readline().replace('\n', '').strip().split(',')
    try:
        no_include = [int(i) for i in user_input]
    except:
        no_include = []
    for i, col in enumerate(lst):
        if i not in no_include:
            r.append(col)
    return ','.join(r)


def filter_ddl(ddl, view, db, schema):
    regexp = re.compile('(.*select)(.*)(from.*)', re.IGNORECASE)
    start = regexp.search(ddl).group(1)
    cols = regexp.search(ddl).group(2).strip()
    end = regexp.search(ddl).group(3)
    filtered_cols = filter_columns(cols, view, db, schema)
    new_ddl = f'{start} {filtered_cols} {end}'
    return new_ddl


def parser(cmd: str):
    cmd = cmd.replace('\n', '')
    ls = cmd.split(' ')
    if ls[0] == 'use' and len(ls) != 3:
        return None
    elif ls[0] == 'copy' and ls[1] != 'views':
        return None
    elif ls[0] == 'copy' and len(ls) == 3:
        if ls[2] != 'filter':
            return None
    elif ls[0] == 'show' and ls[1] != 'views':
        return None
    elif ls[0] == 'sql' and len(ls) < 2:
        return None
    return ls
