from plone import api
from zope.component import getMultiAdapter
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zExceptions import Unauthorized
from zope.globalrequest import getRequest
from zope.interface import alsoProvides
import json
from datetime import datetime
import AccessControl

class FindPost(Service):
    """Search the catalog for HOA Content Type and Return Results """

    def reply(self):
        portal = api.portal.get()
        current = api.user.get_current()
        roles=api.user.get_roles(user=current)
        request = self.request
        context = self.context
        pass