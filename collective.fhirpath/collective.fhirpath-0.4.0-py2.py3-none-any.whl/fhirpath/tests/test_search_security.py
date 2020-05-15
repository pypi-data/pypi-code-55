# _*_ coding: utf-8 _*_
from .base import BaseFunctionalTesting
from .base import FHIR_FIXTURE_PATH
from .base import PATIENT_USER2_NAME
from .base import PATIENT_USER_NAME
from .base import PRACTITIONER_USER_NAME
from collective.elasticsearch.es import ElasticSearchCatalog
from fhirpath.enums import FHIR_VERSION
from fhirpath.interfaces import IElasticsearchEngineFactory
from fhirpath.interfaces import IFhirSearch
from fhirpath.interfaces import ISearchContextFactory
from plone import api
from plone.app.testing import logout
from zope.component import queryMultiAdapter

import json
import os
import time
import uuid


__author__ = "Md Nazrul Islam <email2nazrul@gmail.com>"


class SearchSecurityFunctionalTest(BaseFunctionalTesting):
    """ """

    def get_es_catalog(self):
        """ """
        return ElasticSearchCatalog(api.portal.get_tool("portal_catalog"))

    def get_factory(self, resource_type, unrestricted=False):
        """ """
        factory = queryMultiAdapter(
            (self.get_es_catalog(),), IElasticsearchEngineFactory
        )
        engine = factory(fhir_release=FHIR_VERSION.STU3)
        context = queryMultiAdapter((engine,), ISearchContextFactory)(
            resource_type, unrestricted=unrestricted
        )

        factory = queryMultiAdapter((context,), IFhirSearch)
        return factory

    def load_contents(self):
        """ """
        result = BaseFunctionalTesting.load_contents(self)
        org1_url = result[0]
        # add patient
        self.admin_browser.open(org1_url + "/++add++Patient")
        self.admin_browser.getControl(
            name="form.widgets.IBasic.title"
        ).value = "Test Patient Two"

        with open(os.path.join(FHIR_FIXTURE_PATH, "Patient.json"), "r") as f:
            data = json.load(f)
            data["id"] = str(uuid.uuid4())
            self.admin_browser.getControl(
                name="form.widgets.patient_resource"
            ).value = json.dumps(data)

        self.admin_browser.getControl(name="form.buttons.save").click()
        self.assertIn("Item created", self.admin_browser.contents)
        patient2_url = self.admin_browser.url.replace("/view", "")
        result.append(patient2_url)
        return result

    def test_permission_aware_search(self):
        """ """
        items = self.load_contents()
        practitioner_user = api.user.get(username=PRACTITIONER_USER_NAME)

        org1_url = items[0]

        org_id = org1_url.split("/")[-1]
        brain = api.portal.get_tool("portal_catalog")(
            portal_type="Organization", id=[org_id]
        )
        organization = brain[0].getObject()
        api.user.grant_roles(
            user=practitioner_user, obj=organization, roles=["Practitioner"]
        )

        patient1_url = items[3]
        patient_id = patient1_url.split("/")[-1]

        brain = api.portal.get_tool("portal_catalog")(
            portal_type="Patient", id=[patient_id]
        )
        patient = brain[0].getObject()

        patient_user = api.user.get(username=PATIENT_USER_NAME)
        api.user.grant_roles(user=patient_user, obj=patient, roles=["Patient"])
        api.user.grant_roles(
            user=patient_user, obj=organization, roles=["OrganizationMember"]
        )

        patient2_url = items[-1]
        patient_id = patient2_url.split("/")[-1]

        brain = api.portal.get_tool("portal_catalog")(
            portal_type="Patient", id=[patient_id]
        )
        patient2 = brain[0].getObject()
        patient_user2 = api.user.get(username=PATIENT_USER2_NAME)
        api.user.grant_roles(user=patient_user2, obj=patient2, roles=["Patient"])
        api.user.grant_roles(
            user=patient_user2, obj=organization, roles=["OrganizationMember"]
        )
        # Update Index
        organization.reindexObjectSecurity()
        self.commit()
        time.sleep(1)
        logout()
        params = [("_lastUpdated", "2010-05-28T05:35:56+00:00")]
        search_factory = self.get_factory("Organization", unrestricted=False)
        with api.env.adopt_user(username=PATIENT_USER_NAME):
            bundle = search_factory(params)
            # patient one should have access on his own organization
            self.assertEqual(len(bundle.entry), 1)
            self.assertEqual(bundle.entry[0].resource.id, "f001")

            params = [("gender", "male")]
            search_factory = self.get_factory("Patient", unrestricted=False)
            bundle = search_factory(params)

            # Although First organization have to two patients,
            # but should access it's own.
            self.assertEqual(len(bundle.entry), 1)
            self.assertEqual(
                bundle.entry[0].resource.id, "19c5245f-89a8-49f8-b244-666b32adb92e"
            )

            params = [("status", "ready")]
            search_factory = self.get_factory("Task", unrestricted=False)
            bundle = search_factory(params)
            self.assertEqual(len(bundle.entry), 2)

        with api.env.adopt_user(username=PRACTITIONER_USER_NAME):
            params = [("active", "true")]
            search_factory = self.get_factory("Organization", unrestricted=False)
            bundle = search_factory(params)
            # still single organization
            self.assertEqual(len(bundle.entry), 1)

            params = [("gender", "male")]
            search_factory = self.get_factory("Patient", unrestricted=False)
            bundle = search_factory(params)

            # First organization have to two patients,
            # should access both.
            self.assertEqual(len(bundle.entry), 2)

            params = [("status:not", "rejected")]
            search_factory = self.get_factory("Task", unrestricted=False)
            bundle = search_factory(params)

            self.assertEqual(len(bundle.entry), 3)

        with api.env.adopt_user(username=PATIENT_USER2_NAME):
            params = [("active", "true")]
            search_factory = self.get_factory("Organization", unrestricted=False)
            bundle = search_factory(params)
            # still single organization
            self.assertEqual(len(bundle.entry), 1)

            params = [("gender", "male")]
            search_factory = self.get_factory("Patient", unrestricted=False)
            bundle = search_factory(params)

            self.assertEqual(len(bundle.entry), 1)
            self.assertNotEqual(
                bundle.entry[0].resource.id, "19c5245f-89a8-49f8-b244-666b32adb92e"
            )
