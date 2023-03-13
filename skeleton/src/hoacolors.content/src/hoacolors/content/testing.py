# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import hoacolors.content


class HoacolorsContentLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=hoacolors.content)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "hoacolors.content:default")


HOACOLORS_CONTENT_FIXTURE = HoacolorsContentLayer()


HOACOLORS_CONTENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(HOACOLORS_CONTENT_FIXTURE,),
    name="HoacolorsContentLayer:IntegrationTesting",
)


HOACOLORS_CONTENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(HOACOLORS_CONTENT_FIXTURE,),
    name="HoacolorsContentLayer:FunctionalTesting",
)


HOACOLORS_CONTENT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        HOACOLORS_CONTENT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="HoacolorsContentLayer:AcceptanceTesting",
)
