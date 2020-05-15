import sys
from pathlib import Path
from unittest import mock
from unittest import TestCase

from lxml import etree

from xsdata.formats.dataclass.parsers.nodes import SkipNode
from xsdata.models.elements import Any
from xsdata.models.elements import Attribute
from xsdata.models.elements import AttributeGroup
from xsdata.models.elements import ComplexType
from xsdata.models.elements import DefaultOpenContent
from xsdata.models.elements import Element
from xsdata.models.elements import Extension
from xsdata.models.elements import Import
from xsdata.models.elements import Include
from xsdata.models.elements import OpenContent
from xsdata.models.elements import Override
from xsdata.models.elements import Redefine
from xsdata.models.elements import Restriction
from xsdata.models.elements import Schema
from xsdata.models.enums import FormType
from xsdata.models.enums import Mode
from xsdata.models.enums import Namespace
from xsdata.parser import SchemaParser


class SchemaParserTests(TestCase):
    def setUp(self):
        self.parser = SchemaParser()
        super().setUp()

    def test_complete(self):
        xsd = """<?xml version="1.0" encoding="utf-8"?>
        <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
            <xs:simpleType name="CountryType">
                <xs:annotation>
                  <xs:documentation>
                    <keyword>country</keyword>
                  </xs:documentation>
                </xs:annotation>
              </xs:simpleType>
            </xs:schema>"""

        schema = self.parser.from_string(xsd, Schema)
        expected_namespaces = {
            "xlink": "http://www.w3.org/1999/xlink",
            "xml": "http://www.w3.org/XML/1998/namespace",
            "xs": "http://www.w3.org/2001/XMLSchema",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        }

        self.assertIsInstance(schema, Schema)

        self.assertEqual(expected_namespaces, schema.simple_types[0].ns_map)
        self.assertEqual(3, schema.simple_types[0].index)
        self.assertEqual(4, schema.simple_types[0].annotation.index)
        self.assertEqual(5, schema.simple_types[0].annotation.documentations[0].index)

    @mock.patch.object(SchemaParser, "set_namespace_map")
    def test_dequeue_with_skip_node(self, mock_set_namespace_map):
        objects = list()
        queue = [SkipNode(position=0)]
        element = etree.Element("foo")

        result = self.parser.dequeue(element, queue, objects)
        self.assertIsNone(result)
        self.assertEqual(0, mock_set_namespace_map.call_count)

    def test_start_schema(self):
        element = etree.Element("schema")
        self.parser.start_schema(element, None)

        self.assertIsNone(self.parser.element_form)
        self.assertIsNone(self.parser.attribute_form)
        self.assertIsNone(self.parser.default_attributes)

        element.set("elementFormDefault", "qualified")
        element.set("attributeFormDefault", "unqualified")
        element.set("defaultAttributes", "tns:attr")
        self.parser.start_schema(element, None)

        self.assertEqual("qualified", self.parser.element_form)
        self.assertEqual("unqualified", self.parser.attribute_form)
        self.assertEqual("tns:attr", self.parser.default_attributes)

    def test_set_schema_forms_default(self):
        schema = Schema()
        schema.elements.append(Element.create())
        schema.elements.append(Element.create())
        schema.attributes.append(Element.create())
        schema.attributes.append(Element.create())

        self.parser.set_schema_forms(schema)

        self.assertEqual(FormType.UNQUALIFIED, schema.element_form_default)
        self.assertEqual(FormType.UNQUALIFIED, schema.attribute_form_default)

        for child_element in schema.elements:
            self.assertEqual(FormType.QUALIFIED, child_element.form)

        for child_attribute in schema.attributes:
            self.assertEqual(FormType.QUALIFIED, child_attribute.form)

    def test_set_schema_forms(self):
        schema = Schema()
        schema.elements.append(Element.create())
        schema.elements.append(Element.create())
        schema.attributes.append(Element.create())
        schema.attributes.append(Element.create())

        self.parser.element_form = "unqualified"
        self.parser.attribute_form = "qualified"
        self.parser.set_schema_forms(schema)

        self.assertEqual(FormType.UNQUALIFIED, schema.element_form_default)
        self.assertEqual(FormType.QUALIFIED, schema.attribute_form_default)

        for child_element in schema.elements:
            self.assertEqual(FormType.QUALIFIED, child_element.form)

        for child_attribute in schema.attributes:
            self.assertEqual(FormType.QUALIFIED, child_attribute.form)

    @mock.patch.object(SchemaParser, "set_namespace_map")
    def test_set_schema_namespaces(self, mock_set_namespace_map):
        schema = Schema()
        element = etree.Element("schema")

        self.parser.set_schema_namespaces(schema, element)
        self.assertIsNone(schema.target_namespace)

        self.parser.target_namespace = "bar"
        self.parser.set_schema_namespaces(schema, element)
        self.assertEqual("bar", schema.target_namespace)

        schema.target_namespace = "foo"
        self.parser.set_schema_namespaces(schema, element)
        self.assertEqual("foo", schema.target_namespace)

        mock_set_namespace_map.assert_has_calls(
            [
                mock.call(element, schema),
                mock.call(element, schema),
                mock.call(element, schema),
            ]
        )

    def test_set_namespace_map(self):
        schema = Schema()
        element = etree.Element("schema")

        self.parser.set_namespace_map(element, schema)

        expected = {
            "xlink": "http://www.w3.org/1999/xlink",
            "xml": "http://www.w3.org/XML/1998/namespace",
            "xs": "http://www.w3.org/2001/XMLSchema",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        }
        self.assertEqual(expected, schema.ns_map)

        element = etree.Element(
            "schema", nsmap={"foo": "bar", "not": "http://www.w3.org/2001/XMLSchema"}
        )
        schema = Schema()
        expected = {
            "foo": "bar",
            "xlink": "http://www.w3.org/1999/xlink",
            "xml": "http://www.w3.org/XML/1998/namespace",
            "not": "http://www.w3.org/2001/XMLSchema",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        }

        self.parser.set_namespace_map(element, schema)
        self.assertEqual(expected, schema.ns_map)

    def test_add_default_imports(self):
        schema = Schema.create()
        schema.imports.append(Import.create(namespace="foo"))

        self.parser.add_default_imports(schema)
        self.assertEqual(1, len(schema.imports))

        xsi = Namespace.XSI.value
        schema.ns_map["foo"] = xsi
        self.parser.add_default_imports(schema)
        self.assertEqual(2, len(schema.imports))
        self.assertEqual(Import.create(namespace=xsi), schema.imports[0])

    @mock.patch.object(SchemaParser, "resolve_local_path")
    @mock.patch.object(SchemaParser, "resolve_path")
    def test_resolve_schemas_locations(
        self, mock_resolve_path, mock_resolve_local_path
    ):
        schema = Schema.create()
        self.parser.resolve_schemas_locations(schema)

        self.parser.schema_location = Path.cwd()

        mock_resolve_path.side_effect = lambda x: Path.cwd().joinpath(x)
        mock_resolve_local_path.side_effect = lambda x, y: Path.cwd().joinpath(x)

        schema.overrides.append(Override.create(schema_location="o1"))
        schema.overrides.append(Override.create(schema_location="o2"))
        schema.redefines.append(Redefine.create(schema_location="r1"))
        schema.redefines.append(Redefine.create(schema_location="r2"))
        schema.includes.append(Include.create(schema_location="i1"))
        schema.includes.append(Include.create(schema_location="i2"))
        schema.imports.append(Import.create(schema_location="i3", namespace="ns_i3"))
        schema.imports.append(Import.create(schema_location="i4", namespace="ns_i4"))

        self.parser.resolve_schemas_locations(schema)

        mock_resolve_path.assert_has_calls(
            [
                mock.call("o1"),
                mock.call("o2"),
                mock.call("r1"),
                mock.call("r2"),
                mock.call("i1"),
                mock.call("i2"),
            ]
        )

        mock_resolve_local_path.assert_has_calls(
            [mock.call("i3", "ns_i3"), mock.call("i4", "ns_i4")]
        )

        for sub in schema.included():
            self.assertEqual(Path.cwd().joinpath(sub.schema_location), sub.location)

    def test_resolve_path(self):
        self.assertIsNone(self.parser.resolve_path("foo"))
        iam = Path(__file__)

        self.parser.schema_location = iam.as_uri()
        self.assertIsNone(self.parser.resolve_path(""))
        self.assertIsNone(self.parser.resolve_path(None))

        actual = self.parser.resolve_path(iam.name)
        self.assertEqual(iam.as_uri(), actual)

    def test_resolve_local_path(self):
        self.assertIsNone(self.parser.resolve_local_path("foo", "bar"))
        self.assertIsNone(self.parser.resolve_local_path("foo", None))
        self.assertIsNone(self.parser.resolve_local_path(None, None))
        self.assertIsNone(self.parser.resolve_local_path(None, "bar"))

        self.assertEqual(
            Namespace.XSI.location,
            self.parser.resolve_local_path(None, Namespace.XSI.value),
        )

        self.assertEqual(
            Namespace.XSI.location,
            self.parser.resolve_local_path("http://something", Namespace.XSI.value),
        )
        iam = Path(__file__)
        self.parser.schema_location = iam.as_uri()
        self.assertEqual(iam.as_uri(), self.parser.resolve_local_path(iam.name, None))

    def test_end_attribute(self):
        attribute = Attribute()
        element = etree.Element("uno")

        self.parser.end_attribute(attribute, element)
        self.assertIsNone(attribute.form)

        self.parser.attribute_form = "qualified"
        self.parser.end_attribute(attribute, element)
        self.assertEqual(FormType.QUALIFIED, attribute.form)

    def test_end_complex_type(self):
        complex_type = ComplexType()
        not_complex_type = Element()
        element = etree.Element("uno")

        self.parser.end_complex_type(not_complex_type, element)
        self.parser.end_complex_type(complex_type, element)

        self.assertEqual(0, len(complex_type.attribute_groups))
        self.assertIsNone(complex_type.open_content)

        self.parser.default_attributes = "tns:attrs"
        self.parser.end_complex_type(complex_type, element)

        expected = AttributeGroup.create(ref="tns:attrs")
        self.assertEqual([expected], complex_type.attribute_groups)
        self.assertIsNone(complex_type.open_content)

        default_open_content = DefaultOpenContent()
        self.parser.default_attributes = None
        self.parser.default_open_content = default_open_content
        self.parser.end_complex_type(complex_type, element)
        self.assertIs(default_open_content, complex_type.open_content)

        open_content = OpenContent()
        complex_type.open_content = open_content
        self.parser.end_complex_type(complex_type, element)
        self.assertIs(open_content, complex_type.open_content)

    def test_end_default_open_content(self):
        default_open_content = DefaultOpenContent()
        default_open_content.any = Any.create()
        element = etree.Element("uno")

        self.parser.end_default_open_content(default_open_content, element)
        self.assertEqual(default_open_content, self.parser.default_open_content)
        self.assertEqual(0, default_open_content.any.index)

        default_open_content.mode = Mode.SUFFIX
        self.parser.end_default_open_content(default_open_content, element)
        self.assertEqual(sys.maxsize, default_open_content.any.index)

    def test_end_Element(self):
        obj = Element()
        element = etree.Element("uno")

        self.parser.end_element(obj, element)
        self.assertIsNone(obj.form)

        self.parser.element_form = "qualified"
        self.parser.end_element(obj, element)
        self.assertEqual(FormType.QUALIFIED, obj.form)

    def test_end_extension(self):
        extension = Extension()
        not_extension = Element()
        element = etree.Element("uno")

        self.parser.end_extension(not_extension, element)
        self.parser.end_extension(extension, element)

        default_open_content = DefaultOpenContent()
        self.parser.default_open_content = default_open_content
        self.parser.end_extension(extension, element)

        self.assertIs(default_open_content, extension.open_content)

        open_content = OpenContent()
        extension.open_content = open_content
        self.parser.end_extension(extension, element)
        self.assertIs(open_content, extension.open_content)

    def test_end_open_content(self):
        open_content = OpenContent()
        open_content.any = Any.create()
        element = etree.Element("uno")

        self.parser.end_open_content(open_content, element)
        self.assertEqual(0, open_content.any.index)

        open_content.mode = Mode.SUFFIX
        self.parser.end_open_content(open_content, element)
        self.assertEqual(sys.maxsize, open_content.any.index)

    def test_end_restriction(self):
        restriction = Restriction()
        not_restriction = Element()
        element = etree.Element("uno")

        self.parser.end_restriction(not_restriction, element)
        self.parser.end_restriction(restriction, element)

        default_open_content = DefaultOpenContent()
        self.parser.default_open_content = default_open_content
        self.parser.end_restriction(restriction, element)

        self.assertIs(default_open_content, restriction.open_content)

        open_content = OpenContent()
        restriction.open_content = open_content
        self.parser.end_restriction(restriction, element)
        self.assertIs(open_content, restriction.open_content)

    @mock.patch.object(SchemaParser, "resolve_schemas_locations")
    @mock.patch.object(SchemaParser, "add_default_imports")
    @mock.patch.object(SchemaParser, "set_schema_namespaces")
    @mock.patch.object(SchemaParser, "set_schema_forms")
    def test_end_schema(
        self,
        mock_set_schema_forms,
        mock_set_schema_namespaces,
        mock_add_default_imports,
        mock_resolve_schemas_locations,
    ):
        schema = Schema.create()
        element = Element("schema")

        self.parser.end_schema(schema, element)
        mock_set_schema_forms.assert_called_once_with(schema)
        mock_set_schema_namespaces.assert_called_once_with(schema, element)
        mock_add_default_imports.assert_called_once_with(schema)
        mock_resolve_schemas_locations.assert_called_once_with(schema)
