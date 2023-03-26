# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from plone import api


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "hoacolors.policy:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return ["hoacolors.policy.upgrades"]

def setupGroups(portal):
    acl_users = api.portal.get_tool('acl_users')
    if not acl_users.searchGroups(name='HOAmanagers'):
        gtool = api.portal.get_tool('portal_groups')
        gtool.addGroup('HOAmanagers', roles=['HOAmanager'])
    if not acl_users.searchGroups(name='HomeOwners'):
        gtool = api.portal.get_tool('portal_groups')
        gtool.addGroup('HomeOwners', roles=['HomeOwner'])

def importVarious(context):
    """Miscellanous steps import handle
    """
    if context.readDataFile('hoacolors.policy-various.txt') is None:
        return
    portal = context.getSite()
    setupGroups(portal)

def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
