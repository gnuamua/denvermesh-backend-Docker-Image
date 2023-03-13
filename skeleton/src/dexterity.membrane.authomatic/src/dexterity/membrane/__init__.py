# -*- coding: utf-8 -*-
__import__('pkg_resources').declare_namespace(__name__)

from dexterity.membrane.deprecation import deprecate
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('dexterity.membrane')

# Enable deprecations
deprecate()
