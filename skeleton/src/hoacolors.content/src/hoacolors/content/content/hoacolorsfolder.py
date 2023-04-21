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

class IHoacolorsfolder(model.Schema):
    """Dexterity-Schema for Hoacolorsusers content type."""

@implementer(IHoacolorsfolder)
class Hoacolorsfolder(Container):
    """Hoacolorsusers Content type instance class"""