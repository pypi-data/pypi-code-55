# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.sortedcontrolpanels


class CollectiveSortedcontrolpanelsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.sortedcontrolpanels)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.sortedcontrolpanels:default')


COLLECTIVE_SORTEDCONTROLPANELS_FIXTURE = CollectiveSortedcontrolpanelsLayer()


COLLECTIVE_SORTEDCONTROLPANELS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_SORTEDCONTROLPANELS_FIXTURE,),
    name='CollectiveSortedcontrolpanelsLayer:IntegrationTesting',
)


COLLECTIVE_SORTEDCONTROLPANELS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_SORTEDCONTROLPANELS_FIXTURE,),
    name='CollectiveSortedcontrolpanelsLayer:FunctionalTesting',
)


COLLECTIVE_SORTEDCONTROLPANELS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_SORTEDCONTROLPANELS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveSortedcontrolpanelsLayer:AcceptanceTesting',
)
