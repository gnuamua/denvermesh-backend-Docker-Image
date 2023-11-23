# -*- coding: utf-8 -*-
from plone import api
from zope.component import getMultiAdapter
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from zope.securitypolicy.interfaces import IPrincipalRoleMap
from zExceptions import Unauthorized
from zope.globalrequest import getRequest
from zope.interface import alsoProvides
import json
from datetime import datetime
import AccessControl
import random
import transaction


from hoacolors.content import (
    CanSubscribePermission
)

@implementer(IPublishTraverse)
class SubscribePost(Service):
    """Create Subscription Content Type and populate with data"""
    def reply(self):
        portal = api.portal.get()
        request = self.request
        context = self.context
        now = datetime.now()
        # get the request Body info
        data = json.loads(request["BODY"])
        #get current user 'MemberData' object
        current = api.user.get_current()
        #get current user properties and assign them to variables
        current_id = current.getProperty('id')
        current_full_name = data['nameUserFirst']['nameUserFirst'] + " " + data['nameUserLast']['nameUserLast']
        current_email = data['userEmail']['userEmail']
        current_phone = data['phoneNumber']['phoneNumber']
        #update User Information and set Username to userId
        current_properties = dict(
            fullname=current_full_name,
            email=current_email,
            phone_number=current_phone,
        )
        current.setMemberProperties(current_properties)
        #import pdb; pdb.set_trace() 
        roles=api.user.get_roles(user=current)
        can_subscribe = api.user.has_permission(CanSubscribePermission, obj=self.context)
        if not can_subscribe:
            raise Unauthorized("User not authorized to purchase Subscription.")
        # Check CSRF authenticator from frontend
        authenticator = getMultiAdapter((self.context, self.request), name="authenticator")
        if not authenticator.verify():
            raise Unauthorized("User not authorized to purchase Subscription.")
        #check for coded password from Frontend
        subCode = data['subCode']['subCode']
        if not subCode == "Gnuamuya01HOAcolors!?#@$&%":
            raise Unauthorized("User not Authorized to purchase Subscription.")
        #set the group_name variable for the HOAmanagers group
        group_name = "HOAmanagers"
        #Adopt the Manager proxy-role
        with api.env.adopt_roles(['Manager']):
            #add the current user to the HOAmanagers group
            api.group.add_user(groupname=group_name, user=current)
            #assign variables from JSON BODY of request
            nameUserFirst = data['nameUserFirst']['nameUserFirst']
            nameUserLast = data['nameUserLast']['nameUserLast']
            userEmail = data['userEmail']['userEmail']
            phoneNumber = data['phoneNumber']['phoneNumber']
            nameHOA = data['nameHOA']['nameHOA']
            streetAddress = data['streetAddress']['streetAddress']
            cityHOA = data['cityHOA']['cityHOA']
            stateHOA = data['stateHOA']['stateHOA']
            zipCode = data['zipCode']['zipCode']
            fullAddress = data['fullAddress']['fullAddress']
            totalHomes = data['totalHomes']['numberHomes']
            subCode = data['subCode']['subCode']
            subID = data['subID']['orderID']
            price = data['price']['price']
            #Quick coding to create a community code for the subscription
            numCode = random.randint(1000000,10000000)
            numString= 'C' + str(numCode)
            #import pdb; pdb.set_trace()
            #Create the Instance of the Subscription Content Type
            objSubscription = api.content.create(
                type='subscription',
                title=nameHOA,
                container=portal["subscriptions"],
                name_of_hoa=nameHOA,
                email=userEmail,
                first_name=nameUserFirst,
                last_name=nameUserLast,
                phoneNumber=phoneNumber,
                address=fullAddress,
                zipcode=zipCode,
                total_homes=totalHomes,
                subscription_id=subID,
                start=now,
                price=price,
                communityCode=numString,
                )
            #Set the Review State of the Subscription Content Type to 'Subscription Active'
            api.content.transition(objSubscription, to_state="Subscription Active")
            #Create the Instance of the HOA Content Type
            objHOA = api.content.create(
                type='hoa',
                title=nameHOA,
                container=objSubscription,
                name_of_hoa=nameHOA,
                email=userEmail,
                first_name=nameUserFirst,
                last_name=nameUserLast,
                address=fullAddress,
                zipcode=zipCode,
                total_homes=totalHomes,
            )
            #Transition the HOA Instance to 'Subscription Active' state
            api.content.transition(objHOA, to_state="Subscription Active")
            #Set Local Roles and Ownership of the installed Instances of the HOA & Subscription Content Types
            objSubscription.changeOwnership(user=current, recursive=False)
            objHOA.changeOwnership(user=current, recursive=False)
            objSubscription.manage_setLocalRoles(current_id, ['Creator'])
            objHOA.manage_setLocalRoles(current_id, ['Creator'])
            objSubscription.manage_permission('View', roles=['Creator'], acquire=False)
            objHOA.manage_permission('View', roles=['HomeOwner'], acquire=False)
            #Persist the changes in the ZODB
            objSubscription.reindexObject()
            objHOA.reindexObject()
            return
        
