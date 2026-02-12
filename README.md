# mailman-ietf-styles

IETF list styles for Mailman 3. Provides two styles applied at list creation time:

- **ietf-default** — Standard discussion list with `@global-allowlist@ietf.org` in `accept_these_nonmembers`
- **ietf-announce** — Announce-only list (no global allowlist)

## Installation

```
pip install git+https://github.com/ietf-tools/mailman-ietf-styles.git@1.0.0
```

## Configuration

Add to `mailman.cfg`:

```ini
[plugin.ietf_styles]
class: mailman_ietf_styles.plugin.IETFStylesPlugin
enabled: yes
component_package: mailman_ietf_styles

[styles]
default: ietf-default
```

The global allowlist address defaults to `@global-allowlist@ietf.org` and can be overridden with the `GLOBAL_ALLOWLIST_FQDN` environment variable.
