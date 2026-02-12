"""IETF Styles plugin for Mailman 3."""

from mailman.interfaces.plugin import IPlugin
from zope.interface import implementer


@implementer(IPlugin)
class IETFStylesPlugin:
    """Plugin that provides IETF-specific list styles."""

    def pre_hook(self):
        pass

    def post_hook(self):
        pass

    @property
    def resource(self):
        return None
