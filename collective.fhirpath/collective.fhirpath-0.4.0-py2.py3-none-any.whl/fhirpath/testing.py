# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import zope as z2
from zope.configuration import xmlconfig

import os
import pathlib
import sys


TEST_ZCML = """\
<configure
    xmlns="http://namespaces.zope.org/zope">
    <include package="fhir_restapi.services" />
</configure>
"""
EXAMPLE_RESTAPI_DIR = (
    pathlib.Path(os.path.abspath(__file__)).parent.parent.parent.parent / "examples"
)
IS_TRAVIS = "TRAVIS" in os.environ


class CollectiveFhirpathLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)

        import collective.elasticsearch

        self.loadZCML(package=collective.elasticsearch)

        import plone.app.fhirfield

        self.loadZCML(package=plone.app.fhirfield)

        import collective.MockMailHost
        self.loadZCML(package=collective.MockMailHost)

        import collective.fhirpath

        self.loadZCML(package=collective.fhirpath)
        # initialize method not calling automatically
        z2.installProduct(app, "collective.fhirpath")
        # Load Custom
        if str(EXAMPLE_RESTAPI_DIR) not in sys.path[:]:
            sys.path.append(str(EXAMPLE_RESTAPI_DIR))

        xmlconfig.string(TEST_ZCML, context=configurationContext)

    def setUpPloneSite(self, portal):
        """ """
        applyProfile(portal, "collective.elasticsearch:default")
        applyProfile(portal, "plone.app.fhirfield:default")
        applyProfile(portal, "collective.fhirpath:default")
        applyProfile(portal, "collective.fhirpath:testing")


COLLECTIVE_FHIRPATH_FIXTURE = CollectiveFhirpathLayer()


COLLECTIVE_FHIRPATH_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_FHIRPATH_FIXTURE,),
    name="CollectiveFhirpathLayer:IntegrationTesting",
)


COLLECTIVE_FHIRPATH_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_FHIRPATH_FIXTURE,),
    name="CollectiveFhirpathLayer:FunctionalTesting",
)

COLLECTIVE_FHIRPATH_REST_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_FHIRPATH_FIXTURE, z2.WSGI_SERVER_FIXTURE),
    name="CollectiveFhirpathLayer:RestFunctionalTesting",
)
