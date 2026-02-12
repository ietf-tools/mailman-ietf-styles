"""Tests for IETF list styles."""

import importlib
from unittest.mock import MagicMock, patch

from mailman_ietf_styles.styles.ietf import (
    GLOBAL_ALLOWLIST_ADDRESS,
    IETFAnnounceStyle,
    IETFDefaultStyle,
    _add_global_allowlist,
)


def _mock_list():
    mlist = MagicMock()
    mlist.accept_these_nonmembers = []
    return mlist


def test_add_global_allowlist():
    mlist = _mock_list()
    _add_global_allowlist(mlist)
    assert GLOBAL_ALLOWLIST_ADDRESS in mlist.accept_these_nonmembers


def test_add_global_allowlist_handles_none():
    mlist = MagicMock()
    mlist.accept_these_nonmembers = None
    _add_global_allowlist(mlist)
    assert mlist.accept_these_nonmembers == [GLOBAL_ALLOWLIST_ADDRESS]


def test_add_global_allowlist_idempotent():
    mlist = _mock_list()
    _add_global_allowlist(mlist)
    _add_global_allowlist(mlist)
    assert mlist.accept_these_nonmembers.count(GLOBAL_ALLOWLIST_ADDRESS) == 1


@patch('mailman_ietf_styles.styles.ietf._legacy_default')
def test_default_style_calls_legacy_then_adds_allowlist(mock_legacy):
    mlist = _mock_list()
    IETFDefaultStyle().apply(mlist)
    mock_legacy.apply.assert_called_once_with(mlist)
    assert GLOBAL_ALLOWLIST_ADDRESS in mlist.accept_these_nonmembers


@patch('mailman_ietf_styles.styles.ietf._legacy_announce')
def test_announce_style_calls_legacy_no_allowlist(mock_legacy):
    mlist = _mock_list()
    IETFAnnounceStyle().apply(mlist)
    mock_legacy.apply.assert_called_once_with(mlist)
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
