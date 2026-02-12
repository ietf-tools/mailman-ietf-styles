"""IETF default list styles."""

from mailman.config import config
from mailman.interfaces.styles import IStyle

# "Legacy" is upstream Mailman's naming (from the 2->3 migration), not a
# deprecation marker.  These are the standard built-in styles and the only
# concrete IStyle implementations Mailman ships.  We call their apply() first
# to initialise all required list attributes before adding IETF customisations.
from mailman.styles.default import LegacyAnnounceOnly, LegacyDefaultStyle
from zope.interface import implementer

__all__ = [
    'IETFDefaultStyle',
    'IETFAnnounceStyle',
]

DEFAULT_ALLOWLIST_FQDN = '@global-allowlist@ietf.org'

_legacy_default = LegacyDefaultStyle()
_legacy_announce = LegacyAnnounceOnly()


def _get_allowlist_address():
    """Read the global allowlist FQDN from the plugin config in mailman.cfg."""
    for name, section in config.plugin_configs:
        if name == 'ietf_styles':
            return section.get('global_allowlist_fqdn', DEFAULT_ALLOWLIST_FQDN)
    return DEFAULT_ALLOWLIST_FQDN


def _add_global_allowlist(mailing_list):
    """Add the global allowlist to accept_these_nonmembers."""
    address = _get_allowlist_address()
    if not mailing_list.accept_these_nonmembers:
        mailing_list.accept_these_nonmembers = [address]
    elif address not in mailing_list.accept_these_nonmembers:
        mailing_list.accept_these_nonmembers.append(address)


@implementer(IStyle)
class IETFDefaultStyle:
    """IETF discussion list: default settings + global allowlist."""

    name = 'ietf-default'
    description = 'IETF discussion list with global allowlist for cross-posting.'

    def apply(self, mailing_list):
        _legacy_default.apply(mailing_list)
        _add_global_allowlist(mailing_list)


@implementer(IStyle)
class IETFAnnounceStyle:
    """IETF announce list: announce settings, NO global allowlist."""

    name = 'ietf-announce'
    description = 'IETF announce-only list (no global allowlist).'

    def apply(self, mailing_list):
        _legacy_announce.apply(mailing_list)
