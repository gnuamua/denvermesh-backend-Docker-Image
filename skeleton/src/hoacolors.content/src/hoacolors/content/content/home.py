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
            raise zope.interface.Invalid("Zipcode must be 5 digits")
    return True

def lastNameConstraint(value):
    """Check if last name is valid"""
    if value and value == value.lower():
        raise zope.interface.Invalid("Name must have at least one capital letter")
    return True

def firstNameConstraint(value):
    """Check if first name is valid"""
    if value and value == value.lower():
        raise zope.interface.Invalid("Name must have at least one capital letter")
    return True

class IHome(model.Schema):
    """Dexterity-Schema for Home Content type"""

    first_name = schema.TextLine(
        title='First Name',
        description='First name of the Homeowner',
        required=True,
        constraint=firstNameConstraint,
    )

    last_name = schema.TextLine(
        title='Last Name',
        description='Last name of the Homeowner',
        required=True,
        constraint=lastNameConstraint,
    )

    email_homeowner = Email(
        title='Email of Homeowner',
        description='Email address of the Homeowner',
        required=True,
    )

    address = schema.TextLine(
        title='Street Address',
        description='Street Address of the Home to be painted',
        required=True,
    )

    zipcode = schema.Int(
        title='Zipcode',
        description='Zipcode of the Home',
        required=True,
        constraint=zipcodeIsValid,
    )

    name_hoa = schema.TextLine(
        title='Name of HOA',
        description='Current HOA',
        required=True,
    )

@implementer(IHome)
class Home(Container):
    """Home Content type instance class"""