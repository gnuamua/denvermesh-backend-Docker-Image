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

def zipcodeIsValid(value):
    """Check if zipcode is valid"""
    if value:
        if len(value)!= 5:
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
        if valuer <= 0:
            raise zope.interface.Invalid("Total number of homes must be a postive number greater than Zero")
    return True

class ISubscription(model.Schema):
    """Dexterity-Schema for HOA Subscriptions"""

    name_of_hoa= schema.TextLine(
        title='Name of HOA',
        description='The name of the Home Owners Association',
        required=True,
    )

    email = Email(
        title='Email of Manager',
        description='Email adress of the HOA manager',
        required=True,
    )

    first_name = schema.TextLine(
        title='First Name',
        description='First name of the Manager',
        required=True,
        constraint=firstNameConstraint,
    )

    last_name = schema.TextLine(
        title='Last Name',
        description='Last name of the Manager',
        required=True,
        constraint=lastNameConstraint,
    )

    address = schema.TextLine(
        title='Street Address',
        description='Street Address of the HOA to be configured',
        required=True,
    )

    zipcode = schema.Int(
        title='Zipcode',
        description='Zipcode of the HOA',
        required=True,
        constraint=zipcodeIsValid,
    )

    total_homes = schema.Int(
        title='Total Homes',
        description='The total number of Homes in the HOA',
        required=True,
        constraint=totalHomesIsValid,
    )

    start = schema.Datetime(
        title=('Start date'),
        required=False,
    )

    end = schema.Datetime(
        title=('End date'),
        required=False,
    )

@implementer(ISubscription)
class Subscription(Container):
    """Subscription content type instance class"""
