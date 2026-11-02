# Hermes 0.22.5 compatibility (0.5.15)

The manifest now accepts `>=0.22.1,<0.22.6`. The upper bound deliberately excludes
unexercised 0.22.6 and later versions. Earlier release evidence documents 0.22.1;
this page supersedes its compatibility upper bound, not its limitations.

Revalidation used the actual selected Windows PM workspace for Hermes 0.22.5
(canonical host revision `bf0203a794a07aac3ff764972ab9087baa4e4f4e`) and its Python
3.14.9 interpreter, with a disposable HERMES_HOME. The native registry still
registers `browser_vault` actions list/unlock/enter_code/fill/save_login and the
native callback getters/setters retain their scoped bridge contract. The bridge
intercepts only list/unlock/enter_code, leaves other arguments/actions untouched,
and restores callbacks on exit. No core patch, secret-storage, consent, owner,
redaction or retained-destination policy changes were needed.

Acceptance:

- New regression failed on the old manifest rejecting 0.22.5, then passed.
- Actual selected interpreter: 26 registered native bridge tests and 6 action
  contract tests pass (synthetic HTTP/code/unlock and thread handoff only).
- Full suite against the same selected source: 285 tests, 4 existing skips,
  passing in an isolated Python 3.14.9 environment with selected dependencies
  plus test-only Playwright and Telegram SDK. The live interpreter lacks those
  optional test dependencies; it was not modified to add them.
- The only fixture adaptation handles the host's daemon-tracking dict instead
  of the earlier set during disposable browser cleanup. Production Python is
  unchanged. Real Chrome/OOPIF generated-JavaScript and native-consent tests pass.

This is synthetic native integration evidence, not new live-merchant acceptance,
real credential collection, or proof of universal payment-form support. The
payment diagnostic module remains 0.5.14 because its implementation is unchanged.

Install an explicitly verified immutable commit with the supported plugin CLI:

```bash
hermes plugins install https://github.com/mforzano/hermes-secure-entry.git --ref <40-character-commit> --force --yes-deps --enable
hermes plugins doctor secure-entry --ci
```

Before replacing loaded middleware, disable secure-entry, call the native
`gateway.control_socket.reload_gateway_plugins(home)`, and verify unload/listener
shutdown. Then install, reload and use a fresh session for updated tool schemas.
Do not overwrite a loaded listener or modify another profile. Existing Link
configuration, Tailscale-only routing, native consent and exact targets remain
unchanged; no payment or real credential request is needed for compatibility
acceptance.
