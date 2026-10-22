# Founder video or recorded intro

**In one line:** the video is optional, and Tricorder uses it for one thing: hearing the founder state the numbers in their own voice and setting them against the deck.

Written 2026-10-22 for the Tricorder document guides (group: story). Every quote below was checked word for word against the saved page by `raw/_verify_story/verify_quotes_story.py`; the rows are in `quotes_story.csv`. Vendor views are marked. Investor words that reach me only through a news article are paraphrased.

## 1. What it is

A short recording of the founders talking. It comes in four kinds:

- **The application or intro video:** about a minute, founders only. YC sets the form: "The video should be 1 minute long and should contain nothing except the founders talking." ([YC](https://www.ycombinator.com/video/))
- **The pitch video:** a walk through the deck, often around five minutes, that an investor can watch alone. Allison Byers, who is writing a fundraising book for founders outside the usual networks, says: "This is not a replacement for a live meeting, but it’s often what gets you the meeting." ([Allison Byers](https://allisonbyers.beehiiv.com/p/lights-camera-fundraising))
- **The product demo recording** (covered in the roadmap and demo guide).
- **The room walkthrough:** "a 1–3 minute screen recording that shows how the data room is organized, where to start, and what documents are worth paying attention to." ([GoingVC](https://www.goingvc.com/post/what-to-include-in-a-data-room-cover-letter))

The founders make it. It arrives as an mp4 or a link (YouTube unlisted, Loom, the data room platform).

## 2. At seed and at Series A

It is optional at every stage. Visible, a vendor, marks it as a lighter item at all four stages: "A short founder note or recorded intro video is optional and works well at the earliest stages, but it should sit alongside the cover note in /Welcome/ rather than replace it." ([Visible, vendor view](https://visible.vc/blog/what-to-include-in-your-data-room/))

- **Pre-seed and seed:** most useful when the first contact is online. David Rose, founder of Gust (an angel platform), wrote in 2012: "if your initial contact with a potential investor is online, then (at least in the US, although I assume elsewhere as well) a video can be very helpful." He adds: "If you are going around personally to talk to potential high net worth investor to whom you have an introduction, you probably don’t need a video." ([Gust](https://gust.com/blog/how-important-is-a-video-pitch-to-investors-for-an-early-stage-start-up/)) That post is from 2012, so weigh it lightly.
- **Series A:** rare in the room. The lead meets the founders. At a 2025 panel, Technical.ly reports, one investor said his last half-dozen deals were pitched in person rather than over Zoom or slides, and another suggested a 90-second video for the firm's associate or analyst when the principal cannot meet yet ([Technical.ly](https://technical.ly/entrepreneurship/storytelling-to-investors-builders-2025/), paraphrased).
- **What changes for Tricorder:** at no stage is a missing video a problem. When one exists it is a cheap, early source of spoken numbers.

## 3. What a first pass checks

1. Are all the founders in it, speaking? YC: "If you have more than one founder, have all of your founders in the video."
2. How long is it? A minute or two for an intro; more for a deck walk-through.
3. What numbers does the founder say, and what do they mean by them (ARR or run rate, this year or today)?
4. Do the spoken numbers match the deck, the one-pager and the model?
5. Does the founder add a number the deck does not have?
6. Does it sound unrehearsed and plain, or recited and promotional? YC: "For this video, we want to hear how the founders communicate."

## 4. Green flags

- **The founders speak for themselves and plainly.** YC: "Do not recite a written script: Use bullet points instead." The same page asks for no promotional material: "This is not the place to submit a demo or promotional video." ([YC](https://www.ycombinator.com/video/))
- **It is short and easy to start.** Loom, a vendor of video tools, carries a founder's post (the author says he is a former VC): "If your video is one minute or less, there’s a greater chance the prospective investor will just watch it on the spot." ([Loom, vendor view](https://www.loom.com/blog/how-founder-uses-video-demo-pitch))
- **The spoken numbers equal the deck's.** No source states this as a green flag. It follows from the deck-against-model rule in the deck guide, and Tricorder counts a spoken number that matches the deck as a repeat, not as a new source.
- **A walkthrough of the room** (GoingVC quote above) shows the founder can organize and explain.

## 5. Red flags and pitfalls

Common:

- **A spoken number that is bigger or rounder than the deck's.** This is the difference Tricorder looks for. The investor sources on differing numbers apply to it: CRV says that when numbers differ across the deck, model and records, "the gap suggests carelessness or something worse, and either reading damages the deal." ([CRV](https://www.crv.com/content/what-is-a-data-room)) No source I found talks about video specifically, so the application to video is my inference.
- **A recited script or a promotional cut.** The YC instructions above rule both out for an application.
- **A video too long to watch.** Loom's founder-side advice is to split a long video into one-minute pieces and say the length in the email (same Loom page, vendor view).
- **Product claims with no demo.** A video that tells the investor the product does something is a claim, not a demonstration.

Rare but serious:

- **A recording that is not the person.** CNN reported that the engineering firm Arup lost about $25 million when an employee joined a video call whose other participants were fake re-creations of colleagues; Arup confirmed fake voices and images were used ([CNN](https://edition.cnn.com/2024/05/16/tech/arup-deepfake-scam-loss-hong-kong-intl-hnk), paraphrased). That case was against a company, not an investor, and I found no venture case of a synthetic founder video. I include it because a recorded intro is the one room document that can be a convincing copy of a real person. Tricorder cannot tell, so the operator should meet the founders live.

## 6. How Tricorder checks it

**What a script can check**

- `Claim extraction with timestamps` (FRAMEWORKS 4.1): ffmpeg makes a 16 kHz mono WAV, whisper.cpp writes a transcript with segment times, and the script copies `start_s` and `end_s` from the cited segments. The model never writes times. A claim whose quote is not in the cited segments is marked `unverified`. Spoken numbers are parsed ("three million dollars" becomes 3,000,000) and the hedge word stays beside the value.
- `spoken_arr_vs_claims_page` (4.3): for each metric, compare the spoken value with the deck's claim, the model and the rebuilt figure. The pairs with a spoken value use `spoken_tolerance`, which must sit below the 20 percent gap in the Hollis Voice example and at or above `match_tolerance`.
- Before the recording exists, the same scan reads a script, cited by line.
- Proposed `video_basics`: duration, and the number of distinct speakers if the transcript separates them.

**What needs a model to read**

- Which sentences are factual claims, what metric a phrase maps to ("annual recurring revenue" is the deck's "ARR"), and which period the founder means.
- The "interesting moments" scan (4.2) points the operator to parts worth watching. It must not rank by how impressive they sound.
- Every claim must carry the exact words from the transcript.

**What Tricorder cannot check (leave to the operator)**

- Whether the video is real and unedited. Meet the founders live.
- Presence, ease and chemistry between co-founders. That is the partner's judgment.
- Whether the founder is describing today's numbers or a plan.

## 7. Which readout pieces it feeds

- **The pitch itself:** checklist items "Founder video or recorded intro" (id C62) and "Numbers spoken on the video match the deck" (C66).
- Each spoken claim feeds the piece its label names (traction and revenue for ARR, customers for the largest-customer share, burn and runway for runway, and so on).
- A spoken number that differs from the deck is one of the reasons the traction and revenue piece reads weak, and it sits in that piece's drill-down with the timestamp.

## 8. If it is missing

- **Seed and Series A:** neither a gap nor a flag. It is an optional document at every stage and Tricorder does not ask for it by default.
- **Optional ask-list line, if the operator wants it:** "If you have a short recording of the founders introducing the company, please send it."

## 9. In the Hollis Voice room

The room holds no video file. It holds `01_overview/pitch_video_script.md`, a two-minute script "to read out loud on your phone" with a timestamp on each beat from 0:00 to 1:55. The checklist note says the video is recorded from this script, and Tricorder uses the script as the transcript until a recording exists. The script is also in the seed drop.

Planted flag:

- **PF2b (spoken ARR above the deck):** at 0:35 the founder says "we're at about three million dollars in annual recurring revenue". The deck says $2,500,000, the model $2,240,868 and the rebuilt recurring figure is $2,060,868. The answer key's check is `spoken_arr_vs_claims_page`.

Other lines the script repeats:

- **357 clinics (0:50):** matches the deck and the planted PF7 flag (212 clinics pay).
- **"under nine percent of ARR" for the largest customer (0:50):** matches the deck and sits under PF5.
- **"a little over one hundred percent" net revenue retention (0:50):** consistent with the deck's 102.6%, which PF3 contradicts.
- **Nine million dollars, 24 hires, 37 months (1:45):** matches the deck. The round amount is a green flag (the deck, cap table and model agree); the 37 months sits under PF4.

One note on form. YC asks founders not to recite a written script, and this video is recorded from one. That is fine for a test room, but a real recorded intro read from a script would be worth mentioning to the operator.

## 10. Sources

Each page is saved under `raw/founder-video-or-recorded-intro/`.

- YC, the application video: https://www.ycombinator.com/video/ , `ycombinator_com_video.txt`
- Gust, David Rose (2012): https://gust.com/blog/how-important-is-a-video-pitch-to-investors-for-an-early-stage-start-up/ , `gust_com_blog_how_important_is_a_video_pitch_to_investors_for_an_early_stage_start_up.txt`
- Technical.ly, VC roundtable (2025), paraphrased: https://technical.ly/entrepreneurship/storytelling-to-investors-builders-2025/ , `technical_ly_entrepreneurship_storytelling_to_investors_builders_2025_md.txt`
- Allison Byers, "Lights, camera...fundraising": https://allisonbyers.beehiiv.com/p/lights-camera-fundraising , `allisonbyers_beehiiv_com_p_lights_camera_fundraising.txt`
- GoingVC, data room cover letter: https://www.goingvc.com/post/what-to-include-in-a-data-room-cover-letter , `goingvc_com_post_what_to_include_in_a_data_room_cover_letter.txt`
- CRV, what is a data room: https://www.crv.com/content/what-is-a-data-room , `crv_com_content_what_is_a_data_room.txt`
- CNN, Arup deepfake (news), paraphrased: https://edition.cnn.com/2024/05/16/tech/arup-deepfake-scam-loss-hong-kong-intl-hnk , `edition_cnn_com_2024_05_16_tech_arup_deepfake_scam_loss_hong_kong_intl_hnk.txt`
- Vendor views: Visible https://visible.vc/blog/what-to-include-in-your-data-room/ , `visible_vc_blog_what_to_include_in_your_data_room.txt`; Loom https://www.loom.com/blog/how-founder-uses-video-demo-pitch , `loom_com_blog_how_founder_uses_video_demo_pitch.txt`
- Hollis Voice script (synthetic), a copy: `hollis_voice_pitch_video_script.md`
- Saved and read, not quoted: Pilot (accounting vendor) on preparing a YC video https://pilot.com/blog/how-prepare-yc-application-video ; Startup Grind https://www.startupgrind.com/blog/y-combinator-application-video-tutorial/ ; a Video Highlight summary of a YC Startup School talk https://videohighlight.com/v/B5tU2447OK8 ; Walturn https://www.walturn.com/insights/how-to-apply-for-y-combinator-a-comprehensive-guide ; Angel Investors Network on deepfake fraud (educator) https://angelinvestorsnetwork.com/capital-raising/deepfake-fraud-investor-protection
- I found no VC survey of what investors learn from a founder video. The evidence here is YC's own instructions plus anecdote.
