"""IETF default list styles."""

import os

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

GLOBAL_ALLOWLIST_ADDRESS = os.environ.get(
    'GLOBAL_ALLOWLIST_FQDN',
    '@global-allowlist@ietf.org',
)

_legacy_default = LegacyDefaultStyle()
_legacy_announce = LegacyAnnounceOnly()


def _add_global_allowlist(mailing_list):
    """Add the global allowlist to accept_these_nonmembers."""
    if not mailing_list.accept_these_nonmembers:
        mailing_list.accept_these_nonmembers = [GLOBAL_ALLOWLIST_ADDRESS]
    elif GLOBAL_ALLOWLIST_ADDRESS not in mailing_list.accept_these_nonmembers:
        mailing_list.accept_these_nonmembers.append(GLOBAL_ALLOWLIST_ADDRESS)


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
