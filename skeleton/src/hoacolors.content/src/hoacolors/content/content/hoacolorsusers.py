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

class IHoacolorsusers(model.Schema):
    """Dexterity-Schema for Hoacolorsusers content type."""

    first_name = schema.TextLine(
        title='First Name',
        description='First name of the User',
        required=True,
        constraint=firstNameConstraint,
    )

    last_name = schema.TextLine(
        title='Last Name',
        description='Last name of the User',
        required=True,
        constraint=lastNameConstraint,
    )

    email = Email(
        title='Email of User',
        description='Email address of the User',
        required=True,
    )

    home_page = schema.TextLine(
        title='Homepage of User',
        description='Homepage of the User',
        required=False,
    )

@implementer(IHoacolorsusers)
class Hoacolorsusers(Item):
    """Hoacolorsusers Content type instance class"""