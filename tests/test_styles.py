"""Tests for IETF list styles."""

import importlib
from unittest.mock import MagicMock, patch

from mailman_ietf_styles.styles.ietf import (
    GLOBAL_ALLOWLIST_ADDRESS,
    IETFAnnounceStyle,
    IETFDefaultStyle,
)


def _mock_list():
    mlist = MagicMock()
    mlist.accept_these_nonmembers = []
    return mlist


def test_default_style_adds_allowlist():
    mlist = _mock_list()
    IETFDefaultStyle().apply(mlist)
    assert GLOBAL_ALLOWLIST_ADDRESS in mlist.accept_these_nonmembers


def test_default_style_handles_none():
    mlist = MagicMock()
    mlist.accept_these_nonmembers = None
    IETFDefaultStyle().apply(mlist)
    assert mlist.accept_these_nonmembers == [GLOBAL_ALLOWLIST_ADDRESS]


def test_default_style_idempotent():
    mlist = _mock_list()
    style = IETFDefaultStyle()
    style.apply(mlist)
    style.apply(mlist)
    assert mlist.accept_these_nonmembers.count(GLOBAL_ALLOWLIST_ADDRESS) == 1


def test_announce_style_skips_allowlist():
    mlist = _mock_list()
    IETFAnnounceStyle().apply(mlist)
    assert GLOBAL_ALLOWLIST_ADDRESS not in mlist.accept_these_nonmembers


def test_style_names():
    assert IETFDefaultStyle.name == "ietf-default"
    assert IETFAnnounceStyle.name == "ietf-announce"


def test_default_address():
    assert GLOBAL_ALLOWLIST_ADDRESS == "@global-allowlist@ietf.org"


@patch.dict("os.environ", {"GLOBAL_ALLOWLIST_FQDN": "@test@example.com"})
def test_env_override():
    from mailman_ietf_styles.styles import ietf

    importlib.reload(ietf)
    try:
        assert ietf.GLOBAL_ALLOWLIST_ADDRESS == "@test@example.com"
    finally:
        del __import__("os").environ["GLOBAL_ALLOWLIST_FQDN"]
        importlib.reload(ietf)


def test_plugin_interface():
    from mailman.interfaces.plugin import IPlugin

    from mailman_ietf_styles.plugin import IETFStylesPlugin

    plugin = IETFStylesPlugin()
    assert IPlugin.providedBy(plugin)
    assert plugin.resource is None
