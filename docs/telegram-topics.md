# Telegram topic → requester DM native bridge (local fork)

`0.5.15+topics.1`, based on upstream `44a36874a4fd3e81a1eec6591dea87bf92f5436e`.
No core patch, deployment, restart, real account, or live secret test is included.

## Scope and trust

- Only `browser_vault action=enter_code` (without a handle), `list`, and `unlock`
  gain topic admission. List/unlock support the native login workflow; standalone
  add-login/card, payment, remove-card, status and cancel tools stay DM-only.
- Native gateway task-local identity must match the current cached authenticated
  source, including home/profile, platform, group chat, real sender, topic,
  initiating message, session key and session ID. The middleware task ID is
  retained separately; the native browser call is not rebound to the DM.
- Only Telegram `group` sources with a positive numeric thread and human sender
  qualify. Anonymous-admin/channel sentinels, bots, channel actors, missing
  bindings, cron/headless/delegated contexts, rejected routes and mismatches fail
  closed. Native gateway authorization is rechecked before issuance/delivery and
  before handing submitted input to the waiting native callback.
- Destination is exclusively the authenticated sender's numeric Telegram ID.
  No model-supplied destination is accepted. Start the bot in that user's DM first;
  a blocked/unreachable DM cancels the request without a group fallback or retry.
- The link is a short-lived bearer capability. **Tailscale access + possession of
  the link**, not phone identity or Telegram authentication of the web submitter,
  authorizes submission. A recipient can forward it; this is not prevented.
- The web input enters only the existing native prompt callback, never model/tool
  arguments. The original topic worker continues; browser task identity is unchanged.
- Expiry, one-use/CSRF checks, web Cancel, delivered stop/reset/session-end hooks,
  interrupt and unload fences remain. Once handed to native code, cancellation
  cannot promise no write. Stop/reset of one active topic does not cancel another
  active topic's callback. Admission races remain conservatively fail-closed.
- A newer message replacing the cached source, cache eviction, or changed gateway
  authorization while waiting causes cancellation at handoff, even when the same
  person sent the new message. Do not send another topic message while filling.
  Normal successful turn-end does not itself mean session cancellation.

## Delivery and update coupling

The native `send_message_tool` mirrors sent content through
`_mirror_sent_message`/`gateway.mirror`; its Telegram formatting path also has
retries. Topic capabilities must not enter either path. The plugin uses the SAME
native active-profile config resolver, relay-egress guard and credential snapshot,
then native `_telegram_bot` and `_send_telegram_message_with_retry(attempts=1)` with
plain text and disabled previews. No tool dispatch, transcript mirror, adapter
fallback or session-context rewriting occurs. Exceptions never leave this path as
text. Existing DM behavior is intentionally unchanged and may mirror its links.

This is private-API coupling, NOT a promise of future update compatibility. The
integration suite uses real Hermes middleware, native vault handler/callbacks,
authorization and egress policy, with synthetic transport/supervisor and loopback
HTTP. It was exercised against isolated Hermes 0.22.3 source
`5b147ab036d6d19131bff8d20701b5001eab844a`. The inherited manifest version range does
not imply this topic exception has been verified on every version in that range.
Missing/changed private APIs fail closed. Review these contracts and rerun tests
on every Hermes update; never solve breakage by disabling auth or editing core.

## Deployment checklist (operator/parent only)

1. Independently review the uncommitted fork and tests, especially topic source
   correlation, private send/egress and scoped lifecycle cancellation.
2. Pin the reviewed fork revision and retain upstream rollback. Do not auto-update
   the live plugin from a moving branch. Keep the existing trusted HTTPS/Tailscale
   Serve origin and loopback listener; no public Funnel or group-link fallback.
3. Coordinate plugin replacement/restart outside active requests. This work does
   not perform deployment or change config.
4. With explicit approval, test a dummy OTP from an authorized topic. Verify the
   DM receives the link, topic/transcript gets no capability, and the original
   browser task continues. Test blocked DM, cancellation, another user/topic and
   a native existing DM before using a real login.
5. Full upstream suite contains Windows-only private-card/ACL tests. On macOS those
   are a validation blocker, not evidence of a topic failure or a passing full suite.
