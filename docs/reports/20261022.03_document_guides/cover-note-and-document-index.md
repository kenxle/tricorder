# Cover note and document index

**In one line:** a good cover note and index tell the operator what is in the room and where to start. The check that matters most is whether the index matches the files.

Written 2026-10-22 for the Tricorder document guides (group: story). Every quote below was checked word for word against the saved page by `raw/_verify_story/verify_quotes_story.py`; the rows are in `quotes_story.csv`. Vendor posts (data room sellers) are marked as vendor views.

## 1. What it is

The cover note is a one-page letter that sits at the top of the data room. It says what the founder is raising, what the room holds, and how to reach them. The index is a list of every file with a short description. The founder prepares both, often with the finance lead, and usually as a PDF or a Google Doc in a folder named "Welcome" or "00". Some founders add a one to three minute screen recording that walks through the folders.

Visible, a vendor that sells investor-update software, describes the note this way: "it has three short paragraphs: what you're raising and on what terms, what's inside the data room and where to start, and how to reach you with questions." ([Visible, vendor view](https://visible.vc/blog/what-to-include-in-your-data-room/))

## 2. At seed and at Series A

- **Seed:** expected, and short. Visible's checklist (vendor view) marks the cover note as included at every stage and the document index as a lighter version at pre-seed, then included from seed on ([Visible](https://visible.vc/blog/what-to-include-in-your-data-room/)). A seed room is small. Papermark, another room vendor, describes a YC-stage room this way: "It is 24 files, organised into six folders, shared on a link you control." ([Papermark, vendor view](https://www.papermark.com/blog/data-room-for-yc-startups))
- **Series A:** expected, and it does more work. The room is larger and has more readers (partners, counsel, accountants). Peony, a data room vendor, says the first tier a partner sees before a term sheet should include "a short data index" ([Peony, vendor view](https://www.peony.ink/blog/series-a-data-room)). Hustle Fund's Angel Squad, an angel community that learns from the fund, says the room matters more as the company grows: "If a Series A company sends you a messy Google Drive with unlabeled files and missing documents, that is a real signal." ([Hustle Fund](https://www.hustlefund.vc/post/angel-squad-why-startup-data-rooms-matter-for-investors-and-what-to-actually-look-for))
- **What changes:** at seed the note frames a handful of files. At Series A it also has to say which files are in the first tier, which are held back until a first meeting, and how current each one is.

Hustle Fund's diligence checklist asks for the same thing at the earliest stages, and adds a limit: "Ask for one organized folder with a current index." and "A beautiful data room cannot repair a false metric, missing ownership, or a broken financing record." ([Hustle Fund](https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step))

## 3. What a first pass checks

In this order:

1. Is there a note at the top of the room, and does it say what to open first?
2. Can the operator find the deck, the model and the cap table from it in under a minute? Ellty, a room vendor, says: "If they can't find the cap table in 30 seconds, that's a red flag." ([Ellty, vendor view](https://www.ellty.com/blog/how-investors-review-a-data-room))
3. Does the index list every file that is in the room, and is every listed file in the room?
4. Does the note state the round (amount, instrument, terms) and the date the numbers are as of?
5. Does it say plainly what is held back (a second tier, an NDA, files not yet made)?
6. Do the round and dates in the note agree with the deck's ask slide and the cap table?
7. Is it a map, or does it re-pitch the deck?

## 4. Green flags

- **The index and the room match.** Visible says the opposite is "the first thing a careful investor will notice": "the gap between what the cover note promises and what the room contains is the first thing a careful investor will notice." ([Visible, vendor view](https://visible.vc/blog/what-to-include-in-your-data-room/)) A match is the quiet green flag.
- **It was written last and says so by being accurate.** "A cover note written first describes what you intend to include; a cover note written last describes what's actually there, which is the only version that holds up under diligence." ([Visible, vendor view](https://visible.vc/blog/what-to-include-in-your-data-room/))
- **It names what is held back.** GoingVC, an angel education program, says the note is the place to say it: "If there are files that are gated, placeholder-only, or require additional steps (like NDA), this is where you say it." ([GoingVC](https://www.goingvc.com/post/what-to-include-in-a-data-room-cover-letter))
- **It keeps to framing.** "Keep it specific, keep it short, and avoid re-pitching the deck." ([Visible, vendor view](https://visible.vc/blog/what-to-include-in-your-data-room/))
- **The room is lean and real.** "A room with placeholder folders for documents you don't yet have signals more inexperience than a leaner room organized around what is real." ([Visible, vendor view](https://visible.vc/blog/what-to-include-in-your-data-room/))
- **Good order is read as a habit.** "Impressive companies have everything organized and easy to find." and "The data room is a window into operational discipline." ([Hustle Fund](https://www.hustlefund.vc/post/angel-squad-why-startup-data-rooms-matter-for-investors-and-what-to-actually-look-for))

## 5. Red flags and pitfalls

Common:

- **The note promises files the room does not hold, or the room holds files the note never mentions.** This is the cover note written first and never updated (Visible quote above). Tricorder can test it by script.
- **Stale files.** "Stale documents: Outdated financials force investors to ask for replacements before they can assess current cash and performance." ([CRV](https://www.crv.com/content/what-is-a-data-room)) CRV is a seed and Series A fund, so this is an investor's own list.
- **A bloated room.** "A bloated data room with 200 documents makes investors suspicious" ([Ellty, vendor view](https://www.ellty.com/blog/how-investors-review-a-data-room)). Ellty's own advice is 40 to 60 focused files.
- **Placeholder folders and unlabeled files** (Visible and Hustle quotes above).
- **Several versions of the truth.** CRV: "Investors expect one cap table file that settles ownership, with nothing else in the room contradicting it." ([CRV](https://www.crv.com/content/what-is-a-data-room))
- **The note is a second pitch.** It repeats the deck, so the two can drift apart.

Rare but serious:

- **A missing basic that the note never mentions.** Hustle Fund's checklist says missing or irreconcilable basics such as formation records, the cap table and financing documents can stall a close (the "organized folder with a current index" source above). The index is where a missing basic is easiest to spot.
- **A note that claims more than the files show** (for example "audited" with no audit report in the room). This is my inference from Visible's point about promises and contents; no source names it as a separate flag.

## 6. How Tricorder checks it

**What a script can check**

- There is no check for this document yet; the checklist marks it "not checked yet". I propose one named `index_vs_files`.
  - `listed` = file paths named in the index; `present` = files in the room folder.
  - `missing_from_room` = `listed` minus `present`; `missing_from_index` = `present` minus `listed`.
  - Strip all whitespace before matching, because a PDF index wraps long file names and two-digit row numbers onto two lines (the Hollis Voice index does this).
  - Allow a short list of known sidecar files (such as `claims.json`) that need not be listed.
- A second proposed check, `as_of_dates`: read the as-of date from the note, the deck cover, the model's assumptions and the last row of the metrics file; report any file dated before the note's date. This is the checklist item "no stale document that disagrees with current numbers", also not checked yet.
- Count the first-tier and second-tier files named in the index, so the readout can say how much of the room it saw.
- The existing check `What the room cannot settle` (entry 1.11 in FRAMEWORKS) writes the ask when a file is missing.

**What needs a model to read**

- Pull out the round amount, instrument and terms, the as-of date, the contact line, and any statement about what is held back. The model must quote the exact words and the page.
- Compare the stated round with the deck's ask slide and the cap table (the existing "ask matches the round" check).
- Say whether the note frames or re-pitches. This is a read, not a flag.

**What Tricorder cannot check (leave to the operator)**

- Whether a file was left out on purpose.
- What is in a held-back tier, and whether the founder will share it.
- Whether the data room platform hides folders or limits access in ways the upload did not show.
- Whether anyone at the fund has tracked which folders were opened first (platform analytics are the founder's, not ours).

## 7. Which readout pieces it feeds

- **The pitch itself.** The checklist item "Cover note and document index" (id C59) sits here. Today it feeds the "what is in the room" coverage count and the ask list, not a strong or weak verdict.
- **Checklist coverage and the ask list**, through the files the index shows as missing or held back.
- It also supports "no stale document that disagrees with current numbers" (id C69) once `as_of_dates` exists.

## 8. If it is missing

- **Seed:** a gap, not a red flag. Hustle Fund says that at the earliest stages "an incomplete data room is not automatically fatal", and the Tricorder rule is that a missing document is a question for the operator.
- **Series A:** still a gap, but a more important one, because the room is bigger and a map saves the operator time. It is not a flag. Tricorder builds its own file list from what it received, so the loss is the founder's framing, not coverage.
- **Ask-list line:** "Please send a one-page cover note and an index of the room, with one line per file and the date each file is as of. Say which files you are holding back."

## 9. In the Hollis Voice room

The room holds `00_welcome/cover_note_and_index.pdf`, and the seed drop (the thin first tier) carries it too. No flag is planted in it.

What the script `raw/cover-note-and-document-index/hollis_check_index.py` found (output saved beside it):

- The room has 17 files. The index has 16 rows: 11 first-tier and 5 second-tier. The one file it does not list is the `claims.json` sidecar, which the generator adds for the deck's claims page.
- The cover note says the second tier (revenue by customer, the expense ledger, the three customer agreements) is "shared on request after a first meeting". That is a clear statement of what is held back, which is a green sign. It also explains why three planted flags (the pilot counted as ARR, the hidden churn and the customer concentration) cannot be caught from the seed drop alone.
- A script reading the index must handle wrapped text. Rows 10 to 16 wrap their two-digit numbers across two lines, and the file name `order_form_brookline_row.pdf` breaks across two lines.
- The note names the data date (2026-09-30) and calls the room a Series A room. It does not state the amount raised or give a contact line; the $9,000,000 is on deck slide 13 and the email is on the one-page overview. These are gaps in a synthetic note, not planted flags. A real run would put them on the ask list.

## 10. Sources

Each page is saved under `raw/cover-note-and-document-index/`.

- Visible, "What to include in your data room" (vendor view): https://visible.vc/blog/what-to-include-in-your-data-room/ , `visible_vc_blog_what_to_include_in_your_data_room.txt`
- Visible, "How to write a cover letter for your data room" (vendor view): https://visible.vc/blog/data-room-cover-letter , `visible_vc_blog_data_room_cover_letter.txt`
- Hustle Fund Angel Squad, "Why startup data rooms matter": https://www.hustlefund.vc/post/angel-squad-why-startup-data-rooms-matter-for-investors-and-what-to-actually-look-for , `hustlefund_vc_post_angel_squad_why_startup_data_rooms_matter_for_investors_and_what_to_actually_look.txt`
- Hustle Fund Angel Squad, diligence checklist: https://hustlefund.vc/post/angel-squad-angel-investing-due-diligence-checklist-step-by-step , `hustlefund_vc_post_angel_squad_angel_investing_due_diligence_checklist_step_by_step.txt`
- GoingVC, "What to include in a data room cover letter": https://www.goingvc.com/post/what-to-include-in-a-data-room-cover-letter , `goingvc_com_post_what_to_include_in_a_data_room_cover_letter.txt`
- CRV, "What is a data room": https://www.crv.com/content/what-is-a-data-room , `crv_com_content_what_is_a_data_room.txt`
- Ellty (vendor view): https://www.ellty.com/blog/how-investors-review-a-data-room , `ellty_com_blog_how_investors_review_a_data_room.txt`
- Peony (vendor view): https://www.peony.ink/blog/series-a-data-room , `peony_ink_blog_series_a_data_room.txt`
- Papermark (vendor view): https://www.papermark.com/blog/data-room-for-yc-startups , `papermark_com_blog_data_room_for_yc_startups.txt`
- a16z, insider's guide to data rooms: https://a16z.com/the-insiders-guide-to-data-rooms-what-to-know-before-you-raise/ , `a16z_com_the_insiders_guide_to_data_rooms_what_to_know_before_you_raise.txt`
- Elizabeth Yin's views come through the Hustle Fund Angel Squad post above, written by a Hustle Fund colleague. I did not find her own words on the page, so no quote is attributed to her.
