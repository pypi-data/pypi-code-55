# _*_ coding: utf-8 _*_
from collective.elasticsearch import hook
from collective.elasticsearch.es import ElasticSearchCatalog
from collective.elasticsearch.interfaces import IElasticSettings
from collective.fhirpath.testing import COLLECTIVE_FHIRPATH_FUNCTIONAL_TESTING
from collective.fhirpath.testing import COLLECTIVE_FHIRPATH_REST_FUNCTIONAL_TESTING
from DateTime import DateTime
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from plone.testing import z2
from zope.component import getUtility

import json
import logging
import os
import pathlib
import sys
import transaction
import unittest


__author__ = "Md Nazrul Islam <email2nazrul@gmail.com>"

BASE_TEST_PATH = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
FHIR_FIXTURE_PATH = BASE_TEST_PATH / "fixture" / "FHIR"
PATIENT_USER_NAME = "patient_one"
PATIENT_USER_PASS = "12345"
PATIENT_USER2_NAME = "patient_two"
PATIENT_USER2_PASS = "12345"
PRACTITIONER_USER_NAME = "practitioner_one"
PRACTITIONER_USER_PASS = "12345"


def clearTransactionEntries(es):
    _hook = hook.getHook(es)
    _hook.remove = []
    _hook.index = {}


def tear_down_es(es):
    """ """
    es.connection.indices.delete_alias(index="_all", name=es.index_name)
    es.connection.indices.delete(index="_all")
    clearTransactionEntries(es)


def setup_es(self, es_only_indexes={u"Title", u"Description", u"SearchableText"}):
    """ """
    registry = getUtility(IRegistry)
    settings = registry.forInterface(IElasticSettings, check=False)  # noqa: P001
    # set host
    host = os.environ.get("ES_SERVER_HOST", "127.0.0.1")
    settings.hosts = [host]
    # disable sniffing hosts in tests because docker...
    settings.sniffer_timeout = None
    settings.enabled = True
    settings.sniffer_timeout = 0.0
    settings.es_only_indexes = es_only_indexes

    self.catalog = api.portal.get_tool("portal_catalog")
    self.catalog._elasticcustomindex = "plone-test-index"
    self.es = ElasticSearchCatalog(self.catalog)
    self.catalog.manage_catalogRebuild()


class BaseTesting(unittest.TestCase):
    """" """

    def commit(self):
        transaction.commit()

    def create_member(self, username, password, roles=["Member"], **properties):
        """ """
        acl_users = getattr(self.portal, "acl_users")
        mt = getattr(self.portal, "portal_membership")

        acl_users.userFolderAddUser(username, password, roles=roles, domains=[])
        member = mt.getMemberById(username)  # noqa: P001
        if len(properties) > 0:
            member.setMemberProperties(dict(properties))

        return member

    def enable_event_log(self, loggers=None, plone_log_level="ERROR"):
        """
            :param loggers: dict of loggers. format {'logger name': 'level name'}
            :param plone_log_level: log level of plone. default is ERROR
         """
        defaults = {"collective.fhirpath": "INFO", "collective.elasticsearch": "DEBUG"}
        from Products.CMFPlone.log import logger

        loggers = loggers or defaults

        for logger_name, level_name in loggers.items():
            logging.getLogger(logger_name).setLevel(
                getattr(logging, level_name.upper())
            )
        # Plone log level:
        logger.root.setLevel(getattr(logging, plone_log_level.upper()))

        # Enable output when running tests:
        logger.root.addHandler(logging.StreamHandler(sys.stdout))

    def load_contents(self):
        """ """
        self.admin_browser.open(self.portal_url + "/++add++Organization")

        self.admin_browser.getControl(
            name="form.widgets.IBasic.title"
        ).value = "Test Hospital"

        with open(os.path.join(FHIR_FIXTURE_PATH, "Organization.json"), "r") as f:
            self.admin_browser.getControl(
                name="form.widgets.organization_resource"
            ).value = f.read()
        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)
        org1_url = self.admin_browser.url.replace("/view", "")
        self.admin_browser.open(self.portal_url + "/++add++Organization")
        self.admin_browser.getControl(
            name="form.widgets.IBasic.title"
        ).value = "Hamid Patuary University"
        with open(os.path.join(FHIR_FIXTURE_PATH, "Organization.json"), "r") as f:
            json_value = json.load(f)
            json_value["id"] = "f002"
            json_value["meta"]["lastUpdated"] = "2015-05-28T05:35:56+00:00"
            json_value["meta"]["profile"] = ["http://hl7.org/fhir/Organization"]
            json_value["name"] = "Hamid Patuary University"
            self.admin_browser.getControl(
                name="form.widgets.organization_resource"
            ).value = json.dumps(json_value)
        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)
        org2_url = self.admin_browser.url.replace("/view", "")

        self.admin_browser.open(self.portal_url + "/++add++Organization")
        self.admin_browser.getControl(
            name="form.widgets.IBasic.title"
        ).value = "Call trun University"
        with open(os.path.join(FHIR_FIXTURE_PATH, "Organization.json"), "r") as f:
            json_value = json.load(f)
            json_value["id"] = "f003"
            json_value["meta"]["lastUpdated"] = DateTime().ISO8601()
            json_value["meta"]["profile"] = [
                "http://hl7.org/fhir/Meta",
                "urn:oid:002.160",
            ]
            json_value["name"] = "Call trun University"
            self.admin_browser.getControl(
                name="form.widgets.organization_resource"
            ).value = json.dumps(json_value)
        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)
        org3_url = self.admin_browser.url.replace("/view", "")

        # add patient
        self.admin_browser.open(org1_url + "/++add++Patient")
        self.admin_browser.getControl(
            name="form.widgets.IBasic.title"
        ).value = "Test Patient"

        with open(os.path.join(FHIR_FIXTURE_PATH, "Patient.json"), "r") as f:
            self.admin_browser.getControl(
                name="form.widgets.patient_resource"
            ).value = f.read()

        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)
        patient1_url = self.admin_browser.url.replace("/view", "")

        # add tasks
        self.admin_browser.open(patient1_url + "/++add++Task")
        with open(os.path.join(FHIR_FIXTURE_PATH, "ParentTask.json"), "r") as f:
            json_value = json.load(f)
            self.admin_browser.getControl(
                name="form.widgets.task_resource"
            ).value = json.dumps(json_value)

            self.admin_browser.getControl(
                name="form.widgets.IBasic.title"
            ).value = json_value["description"]

        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)
        task1_url = self.admin_browser.url.replace("/view", "")

        self.admin_browser.open(patient1_url + "/++add++Task")
        with open(os.path.join(FHIR_FIXTURE_PATH, "SubTask_HAQ.json"), "r") as f:
            json_value = json.load(f)
            self.admin_browser.getControl(
                name="form.widgets.task_resource"
            ).value = json.dumps(json_value)

            self.admin_browser.getControl(
                name="form.widgets.IBasic.title"
            ).value = json_value["description"]

        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)
        task2_url = self.admin_browser.url.replace("/view", "")

        self.admin_browser.open(patient1_url + "/++add++Task")
        with open(os.path.join(FHIR_FIXTURE_PATH, "SubTask_CRP.json"), "r") as f:
            json_value = json.load(f)
            self.admin_browser.getControl(
                name="form.widgets.task_resource"
            ).value = json.dumps(json_value)

            self.admin_browser.getControl(
                name="form.widgets.IBasic.title"
            ).value = json_value["description"]

        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)
        task3_url = self.admin_browser.url.replace("/view", "")

        # ES indexes to be ready
        # Let's flush
        self.es.connection.indices.flush()

        return [
            org1_url,
            org2_url,
            org3_url,
            patient1_url,
            task1_url,
            task2_url,
            task3_url,
        ]

    def tearDown(self):
        """ """
        super(BaseTesting, self).tearDown()
        tear_down_es(self.es)


class BaseFunctionalTesting(BaseTesting):
    """ """

    layer = COLLECTIVE_FHIRPATH_FUNCTIONAL_TESTING

    def setUp(self):
        """ """
        self.portal = self.layer["portal"]
        self.portal_url = api.portal.get_tool("portal_url")()
        self.portal_catalog_url = api.portal.get_tool("portal_catalog").absolute_url()

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        setup_es(self)

        self.anon_browser = z2.Browser(self.layer["app"])
        self.error_setup(self.anon_browser)

        self.admin_browser = z2.Browser(self.layer["app"])
        self.admin_browser.addHeader(
            "Authorization",
            "Basic {0}:{1}".format(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )
        self.error_setup(self.admin_browser)

        self.enable_event_log()
        self.create_member(
            username=PATIENT_USER_NAME,
            password=PATIENT_USER_PASS,
            email=PATIENT_USER_NAME + "@example.org",
        )

        self.create_member(
            username=PATIENT_USER2_NAME,
            password=PATIENT_USER2_PASS,
            email=PATIENT_USER2_NAME + "@example.org",
        )

        self.create_member(
            username=PRACTITIONER_USER_NAME,
            password=PRACTITIONER_USER_PASS,
            email=PRACTITIONER_USER_NAME + "@example.org",
        )
        # need to commit here so all tests start with a baseline
        # of elastic enabled
        self.commit()

    def error_setup(self, browser):
        """ """
        browser.handleErrors = False
        self.portal.error_log._ignored_exceptions = ()

        def raising(self, info):
            import traceback

            traceback.print_tb(info[2])
            print(info[1])  # noqa: T001

        from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog

        SiteErrorLog.raising = raising


class BaseRestFunctionalTesting(BaseTesting):
    """ """

    layer = COLLECTIVE_FHIRPATH_REST_FUNCTIONAL_TESTING

    def setUp(self):
        """ """
        super(BaseRestFunctionalTesting, self).setUp()
