# _*_ coding: utf-8 _*_
from .base import BaseFunctionalTesting
from .base import FHIR_FIXTURE_PATH
from collective.elasticsearch.es import ElasticSearchCatalog
from collective.fhirpath.interfaces import IZCatalogFhirSearch
from collective.fhirpath.zcatalog import zcatalog_fhir_search
from DateTime import DateTime
from fhirpath.enums import FHIR_VERSION
from fhirpath.interfaces import IElasticsearchEngineFactory
from fhirpath.interfaces import ISearchContextFactory
from plone import api
from urllib.parse import urlencode
from zope.component import queryMultiAdapter

import copy
import json
import os
import uuid


__author__ = "Md Nazrul Islam <email2nazrul@gmail.com>"


class ZCatalogSearchFunctional(BaseFunctionalTesting):
    """ """

    def get_es_catalog(self):
        """ """
        return ElasticSearchCatalog(api.portal.get_tool("portal_catalog"))

    def get_context(self, resource_type, unrestricted=False):
        """ """
        factory = queryMultiAdapter(
            (self.get_es_catalog(),), IElasticsearchEngineFactory
        )
        engine = factory(fhir_release=FHIR_VERSION.STU3)
        context = queryMultiAdapter((engine,), ISearchContextFactory)(
            resource_type, unrestricted=unrestricted
        )
        return context

    def test_search_using_zcatalog_factory(self):
        """ """
        self.load_contents()

        params = [("_lastUpdated", "2010-05-28T05:35:56+00:00")]
        context = self.get_context("Organization", True)
        factory = queryMultiAdapter((context,), IZCatalogFhirSearch)

        brains = factory(query_string=urlencode(params))

        self.assertEqual(len(brains), 1)
        params = (
            ("_profile", "http://hl7.org/fhir/Organization"),
            ("identifier", "urn:oid:2.16.528.1|91654"),
            ("type", "http://hl7.org/fhir/organization-type|prov"),
            ("address-postalcode", "9100 AA"),
            ("address", "Den Burg"),
        )
        brains = factory(query_string=urlencode(params))
        self.assertEqual(len(brains), 2)

    def test_catalogsearch_fhir_date_param(self):
        """ """
        self.load_contents()
        # ************ FIXTURES ARE LOADED **************
        # test:1 equal to
        context = self.get_context("Organization", False)
        params = (("_lastUpdated", "2010-05-28T05:35:56+00:00"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        # result should contains only item
        self.assertEqual(len(brains), 1)
        self.assertEqual(brains[0].getObject().organization_resource.id, "f001")

        # test:2 not equal to
        params = (("_lastUpdated", "ne2015-05-28T05:35:56+00:00"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        # result should contains two items
        self.assertEqual(len(brains), 2)

        # test:3 less than
        params = (("_lastUpdated", "lt" + DateTime().ISO8601()),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        # result should contains three items, all are less than current time
        self.assertEqual(len(brains), 3)

        # test:4 less than or equal to
        params = (("_lastUpdated", "le2015-05-28T05:35:56+00:00"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        # result should contains two items,
        # 2010-05-28T05:35:56+00:00 + 2015-05-28T05:35:56+00:00
        self.assertEqual(len(brains), 2)

        # test:5 greater than
        params = (("_lastUpdated", "gt2015-05-28T05:35:56+00:00"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        # result should contains only item
        self.assertEqual(len(brains), 1)
        self.assertEqual(brains[0].getObject().organization_resource.id, "f003")

        # test:6 greater than or equal to
        params = (("_lastUpdated", "ge2015-05-28T05:35:56+00:00"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        # result should contains only item
        self.assertEqual(len(brains), 2)

        # ** Issue: 21 **
        context = self.get_context("Task")
        # test IN/OR
        params = (("authored-on", "2017-08-05T06:16:41,ge2018-08-05T06:16:41"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        # should be two
        self.assertEqual(len(brains), 2)

        params = (("authored-on", "2017-05-07T07:42:17,2019-08-05T06:16:41"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        # Although 2019-08-05T06:16:41 realy does not exists but OR
        # feature should bring One
        self.assertEqual(len(brains), 1)

        params = (("authored-on", "lt2018-08-05T06:16:41,gt2017-05-07T07:42:17"),)

        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        # Keep in mind OR feature! not and that's why expected result 3 not 1 because
        self.assertEqual(len(brains), 3)

    def test_catalogsearch_fhir_token_param(self):
        """Testing FHIR search token type params, i.e status, active"""
        self.load_contents()

        context = self.get_context("Task", False)
        params = (("status", "ready"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))

        # should be two tasks with having status ready
        self.assertEqual(len(brains), 2)

        params = (("status:not", "ready"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))

        # should be one task with having status draft
        self.assertEqual(len(brains), 1)

        # test with combinition with lastUpdated
        params = (("status", "ready"), ("_lastUpdated", "lt2018-01-15T06:31:18+00:00"))

        brains = zcatalog_fhir_search(context, query_string=urlencode(params))

        # should single task now
        self.assertEqual(len(brains), 1)

        # ** Test boolen valued token **
        context = self.get_context("Patient", False)
        params = (("active", "true"),)

        brains = zcatalog_fhir_search(context, query_string=urlencode(params))

        # only one patient
        self.assertEqual(len(brains), 1)

        params = (("active", "false"),)

        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 0)

    def test_catalogsearch_fhir_reference_param(self):
        """Testing FHIR search reference type params, i.e subject, owner"""
        self.load_contents()

        context = self.get_context("Task", False)

        patient_id = "Patient/19c5245f-89a8-49f8-b244-666b32adb92e"

        params = (("owner", patient_id),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))

        # should be two tasks with having status ready
        self.assertEqual(len(brains), 2)

        params = (("owner", "Practitioner/619c1ac0-821d-46d9-9d40-a61f2578cadf"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

        params = (("patient", patient_id),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))

        self.assertEqual(len(brains), 3)

        # with compound query
        params = (("patient", patient_id), ("status", "draft"))
        # should be now only single
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

        # Test with negetive
        params = (("owner:not", "Practitioner/fake-ac0-821d-46d9-9d40-a61f2578cadf"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        # should get all tasks
        self.assertEqual(len(brains), 3)

        # Test with nested reference
        params = (
            ("based-on", "ProcedureRequest/0c57a6c9-c275-4a0a-bd96-701daf7bd7ce"),
        )
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))

        # Should One HAQ sub task
        self.assertEqual(len(brains), 1)

    def test_catalogsearch__profile(self):
        """"""
        self.load_contents()
        # test:1 URI
        context = self.get_context("Organization", False)

        params = (("_profile", "http://hl7.org/fhir/Organization"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        # result should contains two items
        self.assertEqual(len(brains), 2)

    def test_catalogsearch_missing_modifier(self):
        """ """
        results = self.load_contents()
        org1_url = results[0]
        # add another patient
        self.admin_browser.open(org1_url + "/++add++Patient")
        self.admin_browser.getControl(
            name="form.widgets.IBasic.title"
        ).value = "Test Patient"

        with open(str(FHIR_FIXTURE_PATH / "Patient.json"), "r") as f:
            data = json.load(f)
            data["id"] = "20c5245f-89a8-49f8-b244-666b32adb92e"
            data["gender"] = None
            self.admin_browser.getControl(
                name="form.widgets.patient_resource"
            ).value = json.dumps(data)

        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)
        # Let's flush
        self.es.connection.indices.flush()

        # Let's test
        context = self.get_context("Patient", False)

        params = (("gender:missing", "true"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))

        self.assertEqual(1, len(brains))
        self.assertIsNone(brains[0].getObject().patient_resource.gender)

        params = (("gender:missing", "false"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(1, len(brains))
        self.assertIsNotNone(brains[0].getObject().patient_resource.gender)

    def test_missing_modifier_working(self):
        """
        """
        self.load_contents()

        # ------ Test in Complex Data Type -------------
        # Parent Task has not partOf but each child has partOf referenced to parent
        context = self.get_context("Task", True)

        params = (("part-of:missing", "false"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        # should be two
        self.assertEqual(len(brains), 2)

        params = (("part-of:missing", "true"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        # should be one (parent Task)
        self.assertEqual(len(brains), 1)

    def test_catalogsearch_identifier(self):
        """ """
        self.load_contents()
        context = self.get_context("Patient", True)
        params = (("identifier", "240365-0002"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

        # Test with system+value
        params = (("identifier", "CPR|240365-0002"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

        # Test with system only with pipe sign
        params = (("identifier", "UUID|"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

        # Test with value only with pipe sign
        params = (("identifier", "|19c5245f-89a8-49f8-b244-666b32adb92e"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

        # Test with empty result
        params = (("identifier", "CPR|19c5245f-89a8-49f8-b244-666b32adb92e"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 0)

        # Test with text modifier
        params = (("identifier:text", "Plone Patient UUID"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

    def test_catalogsearch_array_type_reference(self):
        """Search where reference inside List """
        self.load_contents()
        context = self.get_context("Task", True)
        params = (
            ("based-on", "ProcedureRequest/0c57a6c9-c275-4a0a-bd96-701daf7bd7ce"),
        )
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        # Search with based on

        self.assertEqual(len(brains), 1)

        # Search with part-of
        # should be two sub tasks
        params = (("part-of", "Task/5df31190-0ed4-45ba-8b16-3c689fc2e686"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 2)

    def test_elasticsearch_sorting(self):
        """Search where reference inside List """
        self.load_contents()

        context = self.get_context("Task", True)
        params = (("status:missing", "false"), ("_sort", "_lastUpdated"))
        # Test ascending order
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))

        self.assertGreater(
            brains[1].getObject().task_resource.meta.lastUpdated.date,
            brains[0].getObject().task_resource.meta.lastUpdated.date,
        )
        self.assertGreater(
            brains[2].getObject().task_resource.meta.lastUpdated.date,
            brains[1].getObject().task_resource.meta.lastUpdated.date,
        )
        # Test descending order
        params = (("status:missing", "false"), ("_sort", "-_lastUpdated"))
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertGreater(
            brains[0].getObject().task_resource.meta.lastUpdated.date,
            brains[1].getObject().task_resource.meta.lastUpdated.date,
        )
        self.assertGreater(
            brains[1].getObject().task_resource.meta.lastUpdated.date,
            brains[2].getObject().task_resource.meta.lastUpdated.date,
        )

    def test_quantity_type_search(self):
        """ """
        results = self.load_contents()

        self.admin_browser.open(results[3] + "/++add++ChargeItem")

        self.admin_browser.getControl(
            name="form.widgets.IBasic.title"
        ).value = "Test Clinical Bill"

        with open(os.path.join(FHIR_FIXTURE_PATH, "ChargeItem.json"), "r") as f:
            fhir_json = json.load(f)

        self.admin_browser.getControl(
            name="form.widgets.chargeitem_resource"
        ).value = json.dumps(fhir_json)
        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)
        self.assertIn("chargeitem/view", self.admin_browser.url)
        # Let's flush
        self.es.connection.indices.flush()
        # Test so normal
        context = self.get_context("ChargeItem", True)

        # Test ascending order
        params = (("quantity", "5"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

        params = (("quantity", "lt5.1"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

        # Test with value code/unit and system
        params = (("price-override", "gt39.99|urn:iso:std:iso:4217|EUR"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

        # Test with code/unit and system
        params = (("price-override", "40||EUR"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))

        self.assertEqual(len(brains), 1)
        # Test Issue#21
        fhir_json_copy = copy.deepcopy(fhir_json)
        fhir_json_copy["id"] = str(uuid.uuid4())
        fhir_json_copy["priceOverride"].update(
            {"value": 12, "unit": "USD", "code": "USD"}
        )
        fhir_json_copy["quantity"]["value"] = 3
        fhir_json_copy["factorOverride"] = 0.54

        self.admin_browser.open(results[3] + "/++add++ChargeItem")
        self.admin_browser.getControl(
            name="form.widgets.IBasic.title"
        ).value = "Test Clinical Bill (USD)"
        self.admin_browser.getControl(
            name="form.widgets.chargeitem_resource"
        ).value = json.dumps(fhir_json_copy)
        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)

        fhir_json_copy = copy.deepcopy(fhir_json)
        fhir_json_copy["id"] = str(uuid.uuid4())
        fhir_json_copy["priceOverride"].update(
            {"value": 850, "unit": "BDT", "code": "BDT"}
        )
        fhir_json_copy["quantity"]["value"] = 8
        fhir_json_copy["factorOverride"] = 0.21

        self.admin_browser.open(results[3] + "/++add++ChargeItem")
        self.admin_browser.getControl(
            name="form.widgets.IBasic.title"
        ).value = "Test Clinical Bill(BDT)"
        self.admin_browser.getControl(
            name="form.widgets.chargeitem_resource"
        ).value = json.dumps(fhir_json_copy)
        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)
        # Let's flush
        self.es.connection.indices.flush()

        params = (
            (
                "price-override",
                "gt39.99|urn:iso:std:iso:4217|EUR,le850|urn:iso:std:iso:4217|BDT",
            ),
        )
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))

        self.assertEqual(len(brains), 2)

        params = (("price-override", "ge12,le850"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        # should be all three now
        self.assertEqual(len(brains), 3)
        # serach by only system and code
        params = (
            (
                "price-override",
                (
                    "|urn:iso:std:iso:4217|USD,"
                    "|urn:iso:std:iso:4217|BDT,"
                    "|urn:iso:std:iso:4217|DKK"
                ),
            ),
        )
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        # should be 2
        self.assertEqual(len(brains), 2)

        # serach by unit only
        params = (("price-override", "|BDT,|DKK"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        # should be one
        self.assertEqual(len(brains), 1)

    def test_number_type_search(self):
        """ """
        results = self.load_contents()

        self.admin_browser.open(results[3] + "/++add++ChargeItem")

        self.admin_browser.getControl(
            name="form.widgets.IBasic.title"
        ).value = "Test Clinical Bill"

        with open(os.path.join(FHIR_FIXTURE_PATH, "ChargeItem.json"), "r") as f:
            fhir_json_charge_item = json.load(f)

        self.admin_browser.getControl(
            name="form.widgets.chargeitem_resource"
        ).value = json.dumps(fhir_json_charge_item)
        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)

        # Let's flush
        self.es.connection.indices.flush()
        # Test so normal
        context = self.get_context("ChargeItem", True)

        # Test normal float value order
        params = (("factor-override", "0.8"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

        params = (("factor-override", "gt0.79"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

        # Test for Encounter
        self.admin_browser.open(results[3] + "/++add++Encounter")

        self.admin_browser.getControl(
            name="form.widgets.IBasic.title"
        ).value = "Test Encounter"

        with open(os.path.join(FHIR_FIXTURE_PATH, "Encounter.json"), "r") as f:
            fhir_json = json.load(f)

        self.admin_browser.getControl(
            name="form.widgets.encounter_resource"
        ).value = json.dumps(fhir_json)
        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)
        # Let's flush
        self.es.connection.indices.flush()

        context = self.get_context("Encounter", True)

        params = (("length", "gt139"),)

        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

        # Test Issue#21
        fhir_json_copy = copy.deepcopy(fhir_json_charge_item)
        fhir_json_copy["id"] = str(uuid.uuid4())
        fhir_json_copy["priceOverride"].update(
            {"value": 12, "unit": "USD", "code": "USD"}
        )
        fhir_json_copy["quantity"]["value"] = 3
        fhir_json_copy["factorOverride"] = 0.54

        self.admin_browser.open(results[3] + "/++add++ChargeItem")
        self.admin_browser.getControl(
            name="form.widgets.IBasic.title"
        ).value = "Test Clinical Bill (USD)"
        self.admin_browser.getControl(
            name="form.widgets.chargeitem_resource"
        ).value = json.dumps(fhir_json_copy)
        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)

        fhir_json_copy = copy.deepcopy(fhir_json_charge_item)
        fhir_json_copy["id"] = str(uuid.uuid4())
        fhir_json_copy["priceOverride"].update(
            {"value": 850, "unit": "BDT", "code": "BDT"}
        )
        fhir_json_copy["quantity"]["value"] = 8
        fhir_json_copy["factorOverride"] = 0.21

        self.admin_browser.open(results[3] + "/++add++ChargeItem")
        self.admin_browser.getControl(
            name="form.widgets.IBasic.title"
        ).value = "Test Clinical Bill(BDT)"
        self.admin_browser.getControl(
            name="form.widgets.chargeitem_resource"
        ).value = json.dumps(fhir_json_copy)
        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)
        # Let's flush
        self.es.connection.indices.flush()
        # Test with multiple equal values
        context = self.get_context("ChargeItem", True)
        params = (("factor-override", "0.8,0.21"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 2)

        params = (("factor-override", "gt0.8,lt0.54"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))

        self.assertEqual(len(brains), 1)

    def test_code_datatype(self):
        """ """
        results = self.load_contents()

        self.admin_browser.open(results[3] + "/++add++ChargeItem")

        self.admin_browser.getControl(
            name="form.widgets.IBasic.title"
        ).value = "Test Clinical Bill"

        with open(os.path.join(FHIR_FIXTURE_PATH, "ChargeItem.json"), "r") as f:
            fhir_json = json.load(f)

        self.admin_browser.getControl(
            name="form.widgets.chargeitem_resource"
        ).value = json.dumps(fhir_json)
        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)
        # Let's flush
        self.es.connection.indices.flush()

        # Test code (Coding)
        context = self.get_context("ChargeItem", True)

        params = (("code", "F01510"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

        # Test with system+code
        params = (("code", "http://snomed.info/sct|F01510"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

        # test with code only
        params = (("code", "|F01510"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

        # test with system only
        params = (("code", "http://snomed.info/sct|"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

        # test with text
        params = (("code:text", "Nice Code"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)
        # test with .as(
        self.admin_browser.open(results[3] + "/++add++MedicationRequest")

        self.admin_browser.getControl(
            name="form.widgets.IBasic.title"
        ).value = "Test Clinical Bill"

        with open(os.path.join(FHIR_FIXTURE_PATH, "MedicationRequest.json"), "r") as f:
            fhir_json = json.load(f)

        self.admin_browser.getControl(
            name="form.widgets.medicationrequest_resource"
        ).value = json.dumps(fhir_json)
        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)
        # Let's flush
        self.es.connection.indices.flush()

        # test with only code
        context = self.get_context("MedicationRequest", True)
        params = (("code", "322254008"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

        # test with system and code
        params = (("code", "http://snomed.info/sct|"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

    def test_address_contactpoint(self):
        """ """
        self.load_contents()

        context = self.get_context("Patient", True)
        params = (("email", "demo1@example.com"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))

        self.assertEqual(len(brains), 1)

        # Test address with multiple paths and value for city
        params = (("address", "Indianapolis"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

        # Test address with multiple paths and value for postCode
        params = (("address", "46240"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

        # Test with single path for state
        params = (("address-state", "IN"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))

        self.assertEqual(len(brains), 1)

    def test_humanname(self):
        """ """
        self.load_contents()

        # test with family name
        context = self.get_context("Patient", True)

        params = (("family", "Saint"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))

        self.assertEqual(len(brains), 1)

        # test with given name (array)
        params = (("given", "Eelector"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))

        self.assertEqual(len(brains), 1)

        # test with full name represent as text
        params = (("name", "Patient Saint"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

    def test_composite_type(self):
        """ """
        results = self.load_contents()

        self.admin_browser.open(results[3] + "/++add++Observation")

        self.admin_browser.getControl(
            name="form.widgets.IBasic.title"
        ).value = "Carbon dioxide in blood"

        with open(os.path.join(FHIR_FIXTURE_PATH, "Observation.json"), "r") as f:
            fhir_json = json.load(f)

        self.admin_browser.getControl(
            name="form.widgets.observation_resource"
        ).value = json.dumps(fhir_json)
        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)

        # Let's flush
        self.es.connection.indices.flush()

        context = self.get_context("Observation", True)
        # Test simple composite
        params = (("code-value-quantity", "http://loinc.org|11557-6&6.2"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

    def test_multiple_params_value(self):
        """ """
        self.load_contents()
        context = self.get_context("Task", True)
        params = [
            ("_lastUpdated", "gt2015-10-15T06:31:18+00:00"),
            ("_lastUpdated", "lt2018-01-15T06:31:18+00:00"),
        ]
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))

        self.assertEqual(len(brains), 1)

    def test_IN_OR(self):
        """ """
        results = self.load_contents()
        new_id = str(uuid.uuid4())
        new_patient_id = str(uuid.uuid4())
        new_procedure_request_id = str(uuid.uuid4())
        self.admin_browser.open(results[3] + "/++add++Task")

        with open(os.path.join(FHIR_FIXTURE_PATH, "SubTask_HAQ.json"), "r") as f:
            json_value = json.load(f)
            json_value["id"] = new_id
            json_value["status"] = "completed"
            json_value["for"]["reference"] = "Patient/" + new_patient_id
            json_value["basedOn"][0]["reference"] = (
                "ProcedureRequest/" + new_procedure_request_id
            )

            self.admin_browser.getControl(
                name="form.widgets.task_resource"
            ).value = json.dumps(json_value)

            self.admin_browser.getControl(
                name="form.widgets.IBasic.title"
            ).value = json_value["description"]

        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)

        # Let's flush
        self.es.connection.indices.flush()

        context = self.get_context("Task", True)
        params = (("status", "ready,draft"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        # should All three tasks
        self.assertEqual(len(brains), 3)

        params = (
            (
                "patient",
                "Patient/19c5245f-89a8-49f8-b244-666b32adb92e,Patient/"
                + new_patient_id,
            ),
        )
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        # should All three tasks + one
        self.assertEqual(len(brains), 4)

        params = (
            (
                "based-on",
                (
                    "ProcedureRequest/0c57a6c9-c275-4a0a-"
                    "bd96-701daf7bd7ce,ProcedureRequest/"
                )
                + new_procedure_request_id,
            ),
        )
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        # should two tasks
        self.assertEqual(len(brains), 2)

    def test_issue_21_code_and_coding(self):
        """Add Support for IN/OR query for token and other if possible search type
        """
        results = self.load_contents()
        with open(os.path.join(FHIR_FIXTURE_PATH, "ChargeItem.json"), "r") as f:
            fhir_json = json.load(f)

        fhir_json_copy = copy.deepcopy(fhir_json)
        fhir_json_copy["id"] = str(uuid.uuid4())
        fhir_json_copy["code"]["coding"] = [
            {
                "code": "387517004",
                "display": "Paracetamol",
                "system": "http://snomed.info/387517004",
            }
        ]
        fhir_json_copy["code"]["text"] = "Paracetamol (substance)"

        self.admin_browser.open(results[3] + "/++add++ChargeItem")
        self.admin_browser.getControl(
            name="form.widgets.IBasic.title"
        ).value = "Test Clinical Bill (USD)"
        self.admin_browser.getControl(
            name="form.widgets.chargeitem_resource"
        ).value = json.dumps(fhir_json_copy)
        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)

        fhir_json_copy = copy.deepcopy(fhir_json)
        fhir_json_copy["id"] = str(uuid.uuid4())
        fhir_json_copy["code"]["coding"] = [
            {
                "code": "387137007",
                "display": "Omeprazole",
                "system": "http://snomed.info/387137007",
            }
        ]
        fhir_json_copy["code"]["text"] = "Omeprazole (substance)"

        self.admin_browser.open(results[3] + "/++add++ChargeItem")
        self.admin_browser.getControl(
            name="form.widgets.IBasic.title"
        ).value = "Test Clinical Bill(BDT)"
        self.admin_browser.getControl(
            name="form.widgets.chargeitem_resource"
        ).value = json.dumps(fhir_json_copy)
        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)
        # Let's flush
        self.es.connection.indices.flush()

        context = self.get_context("ChargeItem", True)

        params = (("code", "387517004,387137007"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 2)

        # Test with system+code with negetive
        params = (
            (
                "code:not",
                (
                    "http://snomed.info/sct|F01510,"
                    "http://snomed.info/387137007|387137007"
                ),
            ),
        )
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

    def test_reference_with_below_above(self):
        """ """
        results = self.load_contents()
        context = self.get_context("Task", True)
        # Should Get All Tasks
        params = (("patient:below", "Patient"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 3)

        self.admin_browser.open(results[3] + "/++add++Observation")
        with open(os.path.join(FHIR_FIXTURE_PATH, "Observation.json"), "r") as f:
            json_value1 = json.load(f)
            self.admin_browser.getControl(
                name="form.widgets.observation_resource"
            ).value = json.dumps(json_value1)

            self.admin_browser.getControl(name="form.widgets.IBasic.title").value = (
                json_value1["resourceType"] + json_value1["id"]
            )

        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)

        device_id = str(uuid.uuid4())
        self.admin_browser.open(results[3] + "/++add++Observation")
        with open(os.path.join(FHIR_FIXTURE_PATH, "Observation.json"), "r") as f:
            json_value = json.load(f)
            json_value["id"] = str(uuid.uuid4())
            json_value["subject"] = {"reference": "Device/" + device_id}
            self.admin_browser.getControl(
                name="form.widgets.observation_resource"
            ).value = json.dumps(json_value)

            self.admin_browser.getControl(name="form.widgets.IBasic.title").value = (
                json_value["resourceType"] + json_value["id"]
            )

        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)
        self.es.connection.indices.flush()

        context = self.get_context("Observation", True)
        # Should One
        params = (("subject:below", "Device"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)

        # Little bit complex
        params = (("subject:below", "Device,Patient"),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 2)

        # Search By Multiple Ids
        params = (
            ("subject:above", device_id + "," + json_value1["subject"]["reference"]),
        )
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 2)

        params = (("subject:above", device_id),)
        brains = zcatalog_fhir_search(context, query_string=urlencode(params))
        self.assertEqual(len(brains), 1)
