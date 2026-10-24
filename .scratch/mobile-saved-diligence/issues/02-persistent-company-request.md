# 02: Prepare and retain a company's request

**What to build:** From a company's working page, the associate opens a request dialog, selects documents, adds custom requests, edits the message and copies it into their own email. They can manually record that it was sent and return later to the same request and outstanding items.

**Blocked by:** 01: Open a saved company readout with traceable evidence.

**Status:** ready-for-agent

- [ ] The request opens over the working page and starts with deduplicated research gaps and stage-appropriate documents, including the existing guidance and reasons for asking.
- [ ] Checking, unchecking and adding an item updates the generated draft. Custom items have stable identities and do not receive invented document guidance.
- [ ] Editing the message and subsequently changing the checklist has explicit behavior that preserves the associate's authored text rather than silently replacing it.
- [ ] Selection, additions and edited text are saved by company through a typed persistence boundary and survive leaving the page, restarting the app and reopening the company. State does not leak between demo companies.
- [ ] Copying never marks the request sent. An explicit Mark as sent action records the selected items and asked-at time, then shows them as Open on the working page. An empty request cannot be marked sent, and repeating the action does not duplicate the same submission.
- [ ] Nothing sends email automatically. The recorded status describes the associate's confirmation, not verified delivery by an email provider.
- [ ] Save and copy failures preserve the draft and expose a retryable error without claiming success.
- [ ] Behavioral tests cover persistence, company isolation, item deduplication and copy-versus-sent state. A native walkthrough covers keyboard use, editing, copying and reopening the request after restart.

Matching incoming evidence to requests is ticket 04. This ticket is independently demonstrable with no room arrival.

## Implementation note — 2026-10-24

The [json-render foundation](../json-render-handoff.md) now renders the native request dialog from RPC and saves drafts locally. This ticket remains open: canonical durable request entities and sent/open/answered lifecycle are not implemented by that slice.
