"""Tests for IETF list styles."""

import tempfile
from unittest.mock import MagicMock, patch

from mailman_ietf_styles.styles.ietf import (
    DEFAULT_ALLOWLIST_FQDN,
    IETFAnnounceStyle,
    IETFDefaultStyle,
    _add_global_allowlist,
    _get_allowlist_address,
)


def _mock_list():
    mlist = MagicMock()
    mlist.accept_these_nonmembers = []
    return mlist


def _mock_plugin_configs(cfg_path=''):
    """Return a generator mimicking config.plugin_configs."""
    section = MagicMock()
    section.__getitem__ = lambda self, key: cfg_path if key == 'configuration' else ''
    return iter([('ietf_styles', section)])


def _write_cfg(fqdn):
    """Write a temporary config file and return its path."""
    f = tempfile.NamedTemporaryFile(mode='w', suffix='.cfg', delete=False)
    f.write(f'[general]\nglobal_allowlist_fqdn: {fqdn}\n')
    f.close()
    return f.name


@patch('mailman_ietf_styles.styles.ietf.config')
def test_add_global_allowlist(mock_config):
    cfg_path = _write_cfg(DEFAULT_ALLOWLIST_FQDN)
    mock_config.plugin_configs = _mock_plugin_configs(cfg_path)
    mlist = _mock_list()
    _add_global_allowlist(mlist)
    assert DEFAULT_ALLOWLIST_FQDN in mlist.accept_these_nonmembers


@patch('mailman_ietf_styles.styles.ietf.config')
def test_add_global_allowlist_handles_none(mock_config):
    cfg_path = _write_cfg(DEFAULT_ALLOWLIST_FQDN)
    mock_config.plugin_configs = _mock_plugin_configs(cfg_path)
    mlist = MagicMock()
    mlist.accept_these_nonmembers = None
    _add_global_allowlist(mlist)
    assert mlist.accept_these_nonmembers == [DEFAULT_ALLOWLIST_FQDN]


@patch('mailman_ietf_styles.styles.ietf.config')
def test_add_global_allowlist_idempotent(mock_config):
    cfg_path = _write_cfg(DEFAULT_ALLOWLIST_FQDN)
    mock_config.plugin_configs = _mock_plugin_configs(cfg_path)
    mlist = _mock_list()
    _add_global_allowlist(mlist)
    mock_config.plugin_configs = _mock_plugin_configs(cfg_path)
    _add_global_allowlist(mlist)
    assert mlist.accept_these_nonmembers.count(DEFAULT_ALLOWLIST_FQDN) == 1


@patch('mailman_ietf_styles.styles.ietf.config')
def test_get_allowlist_address_from_config(mock_config):
    cfg_path = _write_cfg('@custom@example.com')
    mock_config.plugin_configs = _mock_plugin_configs(cfg_path)
    assert _get_allowlist_address() == '@custom@example.com'


@patch('mailman_ietf_styles.styles.ietf.config')
def test_get_allowlist_address_no_plugin(mock_config):
    mock_config.plugin_configs = iter([])
    assert _get_allowlist_address() == DEFAULT_ALLOWLIST_FQDN


@patch('mailman_ietf_styles.styles.ietf.config')
def test_get_allowlist_address_no_config_file(mock_config):
    mock_config.plugin_configs = _mock_plugin_configs('')
    assert _get_allowlist_address() == DEFAULT_ALLOWLIST_FQDN


@patch('mailman_ietf_styles.styles.ietf._legacy_default')
@patch('mailman_ietf_styles.styles.ietf.config')
def test_default_style_calls_legacy_then_adds_allowlist(mock_config, mock_legacy):
    cfg_path = _write_cfg(DEFAULT_ALLOWLIST_FQDN)
    mock_config.plugin_configs = _mock_plugin_configs(cfg_path)
    mlist = _mock_list()
    IETFDefaultStyle().apply(mlist)
    mock_legacy.apply.assert_called_once_with(mlist)
    assert DEFAULT_ALLOWLIST_FQDN in mlist.accept_these_nonmembers


@patch('mailman_ietf_styles.styles.ietf._legacy_announce')
def test_announce_style_calls_legacy_no_allowlist(mock_legacy):
    mlist = _mock_list()
    IETFAnnounceStyle().apply(mlist)
    mock_legacy.apply.assert_called_once_with(mlist)
    assert DEFAULT_ALLOWLIST_FQDN not in mlist.accept_these_nonmembers


def test_style_names():
    assert IETFDefaultStyle.name == "ietf-default"
    assert IETFAnnounceStyle.name == "ietf-announce"


def test_default_address_constant():
    assert DEFAULT_ALLOWLIST_FQDN == "@global-allowlist@ietf.org"


def test_plugin_interface():
    from mailman.interfaces.plugin import IPlugin

    from mailman_ietf_styles.plugin import IETFStylesPlugin

    plugin = IETFStylesPlugin()
    assert IPlugin.providedBy(plugin)
    assert plugin.resource is None
