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
import random
from paypalrestsdk.notifications import WebhookEvent
import requests

class WebhooksPost(Service):
    """Webhook endpoint for PayPal Subscription events callback"""

    def reply(self):
        request = self.request
        context = self.context
        # The payload body sent in the webhook event
        event_body = json.loads(request["BODY"])
        transmission_id = request.get_header("PAYPAL-TRANSMISSION-ID")
        auth_algo = request.get_header("PAYPAL-AUTH-ALGO")
        cert_url - request.get_header("PAYPAL-CERT-URL")
        transmission_sig = request.get_header("PAYPAL-TRANSMISSION-SIG")
        transmission_time = request.get_header("PAYPAL-TRANSMISSION-TIME")
        #webhook_id    --The ID of the webhook as configured in your Paypal Developer Portal account.
        #webhook_event -- A webhook event notification.
        response = WebhookEvent.verify(
            transmission_id, transmission_time, webhook_id, event_body, cert_url, transmission_sig, auth_algo)
        #send response to https://api-m.paypal.com/v1/notifications/verify-webhook-signature