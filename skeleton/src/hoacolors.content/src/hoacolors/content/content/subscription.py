from plone import schema
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage
from plone.schema.email import Email
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.radio import RadioFieldWidget
from zope.interface import implementer
from zope.interface import Invalid
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from z3c.form import validator
from plone.uuid.interfaces import IUUID
from plone.base.utils import getToolByName
import zope.component


def zipcodeIsValid(value):
    """Check if zipcode is valid"""
    if value:
        if len(str(value))!= 5:
            raise ValidationError("Zipcode must be 5 digits")
    return True

def lastNameConstraint(value):
    """Check if last name is valid"""
    if value and value == value.lower():
        raise zope.interface.Invalid("First name must have at least one capital letter")
    return True

def firstNameConstraint(value):
    """Check if first name is valid"""
    if value and value == value.lower():
         raise zope.interface.Invalid("Last name must have at least one capital letter")
    return True

def totalHomesIsValid(value):
    """Check if total Homes is a valid positive number"""
    if value:
        if value <= 0:
            raise zope.interface.Invalid("Total number of homes must be a postive number greater than Zero")
    return True

class ISubscription(model.Schema):
    """Dexterity-Schema for HOA Subscriptions"""

    name_of_hoa= schema.TextLine(
        title=u'Name of HOA',
        description=u'The name of the Home Owners Association',
        required=True,
    )

    email = Email(
        title=u'Email of Manager',
        description=u'Email adress of the HOA manager',
        required=True,
    )

    first_name = schema.TextLine(
        title=u'First Name',
        description=u'First name of the Manager',
        required=True,
        constraint=firstNameConstraint,
    )

    last_name = schema.TextLine(
        title=u'Last Name',
        description=u'Last name of the Manager',
        required=True,
        constraint=lastNameConstraint,
    )

    phoneNumber = schema.TextLine(
        title=u'Phone Number',
        description=u'Phone Number of HOA Manager',
        required=True,
    )

    address = schema.TextLine(
        title=u'Street Address',
        description=u'Street Address of the HOA to be configured',
        required=True,
    )

    zipcode = schema.Int(
        title=u'Zipcode',
        description=u'Zipcode of the HOA',
        required=True,
        constraint=zipcodeIsValid,
    )

    total_homes = schema.Int(
        title=u'Total Homes',
        description=u'The total number of Homes in the HOA',
        required=True,
        constraint=totalHomesIsValid,
    )

    start = schema.Datetime(
        title=u'Start date',
        description=u'Start date of the Monthly Subscription',
        required=False,
    )

    price = schema.TextLine(
        title=u'Price Per Month',
        description=u'Price per Month',
        required=True,
    )

    subscription_id = schema.TextLine(
        title=u'Subscription ID',
        description=u'Subscription ID from PayPal',
        required=True,
    ) 

    communityCode = schema.TextLine(
        title=u'Community Code',
        description=u'The unique Code for each HOA to be used by HomeOwners to create a Home ContentType',
        required=True,
    )


@implementer(ISubscription)
class Subscription(Container):
    """Subscription content type instance class"""
     