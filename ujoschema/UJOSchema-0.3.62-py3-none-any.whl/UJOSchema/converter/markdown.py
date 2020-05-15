#
# Copyright (c) 2018-present, wobe-systems GmbH
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#

""" conversion of a schema into a markdown representation """
import logging
from string import Template
from textwrap import dedent

from UJOSchema.constraints import UjsIn, UjsNotIn
from .base import BaseSchemaConverter

log = logging.getLogger(__name__)


def schema_to_markdown(schema):
    return str(SchemaToMarkdown(schema))


class SchemaToMarkdown(BaseSchemaConverter):
    def convert(self):
        result = ""
        for _, value in self.schema.items():
            result += self.class2string(value)
        return result

    def __str__(self):
        return self.convert()

    def class2string(self, obj):
        type_name = type(obj).__name__.lower()
        try:
            converter_method = getattr(self, type_name)
        except AttributeError:
            log.warning(f"Possibly missing: {type_name}")
        else:
            return converter_method(obj)

        return str(obj)

    def typedef(self, obj):
        s = Template(
            dedent(
                """\
                ## $identifier
    
                $doc
    
                | Identifier  | Type  | Constraints  |
                |-------------|-------|--------------|
                | $identifier | $type | $constraints |
                """
            )
        )

        constraints = ""
        range_tabs = []
        for element in obj.constraint:
            constraints = constraints + "<br>" if constraints != "" else ""
            if isinstance(element, UjsIn):
                c = "in [Values](#" + obj.name + "-in-values)"
                range_tabs.append(element)
            elif isinstance(element, UjsNotIn):
                c = "not in [Values](#" + obj.name + "-not-in-values)"
                range_tabs.append(element)
            else:
                c = self.class2string(element)
            constraints = constraints + c

        d = {
            "identifier": obj.name,
            "type": str(obj.type),
            "doc": "" if not obj.doc else obj.doc,
            "constraints": constraints,
        }

        s = s.substitute(d)

        for range_tab in range_tabs:

            iv = Template(
                dedent(
                    """\
                    
                    ### $headline
    
                    $values
                    """
                )
            )
            if isinstance(range_tab, UjsIn):
                d = {
                    "headline": obj.name + " in Values",
                    "values": self.class2string(range_tab),
                }
            elif isinstance(range_tab, UjsNotIn):
                d = {
                    "headline": obj.name + " not in Values",
                    "values": self.class2string(range_tab),
                }
            else:
                raise TypeError("invalid constraint")

            iv = iv.substitute(d)
            s = s + iv

        return s

    def record(self, record):  # pylint: disable=no-self-use
        md = Template(
            dedent(
                """\
                ## $identifier

                $doc

                Items:

                $items
                """
            )
        )

        d = {"identifier": record.name, "doc": record.doc}

        items = [["Name", "Type", "Doc", "Constraints"]]
        items += [
            [item.name, item.type, item.doc or "", item.constraint or ""]
            for item in record.items
        ]

        d["items"] = to_markdown_table(items)
        return md.substitute(d)

    def object(self, uobject):  # pylint: disable=no-self-use
        md = Template(
            dedent(
                """\
                ## $identifier

                $doc

                Items:

                $items
                """
            )
        )

        d = {"identifier": uobject.name, "doc": uobject.doc or ""}

        items = [["Name", "Type", "Doc", "Constraints"]]
        items += [
            [item.name, item.type or "", item.doc or "", item.constraint or ""]
            for item in uobject.items
        ]

        d["items"] = to_markdown_table(items)
        return md.substitute(d)

    def ujsin(self, obj):
        s = dedent(
            """\
            | Value | Description |
            |-------|-------------|
            """
        )

        for value in obj.values:
            doc = value.doc if value.doc is not None else ""
            s = s + "| " + self.class2string(value) + " | " + doc + " |\n"
        return s

    def ujsnotin(self, obj):
        return self.ujsin(obj)


def to_markdown_table(rows, header=None):
    if header:
        rows = header, *rows

    rows = [[str(val) for val in row] for row in rows]
    columns = zip(*rows)
    column_widths = [max(len(val) for val in col) for col in columns]

    rows.insert(1, ["-" * w for w in column_widths])

    md = ""
    for row in rows:
        justified = (
            value.ljust(column_widths[col_idx]) for col_idx, value in enumerate(row)
        )
        md += f"| {' | '.join(justified)} |  \n"

    return md
