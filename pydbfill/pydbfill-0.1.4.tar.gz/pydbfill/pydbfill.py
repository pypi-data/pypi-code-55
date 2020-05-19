import argparse
import pymysql

from datetime import date, datetime
from random import randint
from typing import Dict
from uuid import uuid4

parser = argparse.ArgumentParser(description="write some shit to some tables")

for arg in ["host", "port", "password", "username", "table", "db"]:
    parser.add_argument(
        f"--{arg}", dest=arg, help=f"the {arg}",
    )

args = parser.parse_args()


def connection(host: str, port: int, username: str, password: str, db: str) -> None:
    """Return a connected object to mysql."""
    connection = pymysql.connect(
        host=host,
        user=username,
        password=password,
        port=port,
        db=db,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )

    return connection


def describe_table(conn: pymysql.Connection, table_name: str) -> None:
    """Return a list of fields and their types for a given table."""
    with conn.cursor() as cursor:
        cursor.execute(f"DESCRIBE {table_name};")
        result = cursor.fetchall()

        # drop auto_incrementing fields
        manual_fields = list(
            filter(lambda field: "auto_increment" not in field["Extra"], result)
        )

        # build the mapping of types
        field_mapping = {}
        for field in manual_fields:
            field_mapping[field["Field"]] = field["Type"]

        return field_mapping


def fill_table(conn: pymysql.Connection, table_name: str, count: int) -> None:
    field_mapping = describe_table(conn, table_name)

    try:
        with conn.cursor() as cursor:
            # remove constraints so they dont ruin our style
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")

            for idx in range(count):
                new_record = {}
                for field_name, field_type in field_mapping.items():
                    if "varchar" in field_type:
                        size = int(field_type.split("(")[1].replace(")", ""))
                        new_record[field_name] = f"'{uuid4().hex[:{size}]}'"
                    elif "char" in field_type:
                        size = int(field_type.split("(")[1].replace(")", ""))
                        new_record[field_name] = f'"{uuid4().hex[:{size}]}"'
                    elif "int" in field_type:
                        # this could be random, or we can just increment it
                        # and this way avoid having to worry about any uniqueness constraint
                        new_record[field_name] = str(idx)
                    elif "date" in field_type:
                        new_record[field_name] = date.today().isoformat()
                    elif "timestamp" in field_type:
                        tmp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                        new_record[field_name] = f"'{tmp}'"
                    else:
                        # idk
                        new_record[field_name] = str(1)

                # TODO: prove this preserves ordering
                sql = f"INSERT INTO {table_name} ({','.join(new_record.keys())}) values ({','.join(new_record.values())})"
                cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    conn = connection(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password,
        db=args.db,
    )

    fill_table(conn, args.table, args.num)
