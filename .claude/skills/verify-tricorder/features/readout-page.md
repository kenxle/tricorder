# Readout page

The readout page shows one room's readout: a synthetic-room banner, the top green and red flags, the overview of pieces, the gaps, the claims that could not be verified, and what to ask the founder for, with a room picker and a "Build readout" button.

## Sub-features

- `page-banner` shows the room's synthetic notice.
- `page-sections` shows the sections labelled `Top flags`, `Overview`, `Gaps`, `Could not verify` and `Ask list`.
- `page-build` builds a readout for the picked room.

## How to get to it (user POV)

- Open the API's root URL in a browser after `apps/web/dist/` is built.
- Pick a room from the select labelled `Room`.
- Press `Build readout`.

## Driving it with control.sh

Preconditions:

- `control.sh doctor` prints `OK` for this run, including the page check.
- The scans and the memo ran on `data_room/hollis_voice` in this run (`control.sh cli bin/smoke data_room/hollis_voice`).

- **Capture the page.** Run `control.sh shot readout-hollis`. The screenshot shows the banner "Synthetic data room for Deal Flow NYC 2026. Not a real company." and the DOM has the sections `Top flags`, `Overview`, `Gaps` and `Ask list`.
- **Check the page matches the API.** Run `control.sh api GET /api/rooms/hollis_voice/readout`. Every gap's `what` in the response appears in the DOM's `Gaps` section.

## Gotchas

- The page opens on `hollis_voice`. The helper cannot pick another room; prove other rooms through the API.
- Until the pieces and top-flags steps are built, `Top flags` reads "No flags yet." and `Overview` reads "No piece verdicts yet." That is the current state, not a failure.
- Without a readout in this run's `out/`, the page falls back to `sample_out/` if one exists, which is not this run's data.
- The style is a placeholder until Ken picks a style direction.
