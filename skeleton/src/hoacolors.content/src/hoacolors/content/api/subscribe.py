# -*- coding: utf-8 -*-
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zExceptions import Unauthorized
from zope.globalrequest import getRequest
from zope.interface import alsoProvides

class SubscribeGet(Service):
    """Subscription API Key information for paypal payment processing"""

    def reply(self):
        current = api.user.get_current()
        roles = api.user.get_roles(user=current)
        if ('Authenticated' in roles):
            can_view_subscribe_info = True
        if not can_view_subscribe_info:
            raise Unauthorized("User not authorized to view votes.")
        return subscribe_info(self.context, self.request)

def subscribe_info(obj, request=None):
    """Returns voting information about the given object."""
    if not request:
        request = getRequest()
    info = {
        "total_votes": 0
    }
    return info