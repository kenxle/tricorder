# Cleanup needed

Files agents would delete but may not. Ken removes them in one batch.

- docs/reports/20261022.02_research/raw/voc/_tail_backup.md (R1 temporary backup)
- docs/reports/20261022.02_research/raw/landscape/: R2 says these are optional removals. Stub or error pages: pitchbook_pricing.*, carta_pricing.*, crunchbase_pricing.*, crunchbase_pricing2.*, crunchbase_buy.*, nyu_stern_vc_class.*, partisia_*, f4_yaven.*, akta_home.*, akta_site.*, akta_pricing_web.*, akta_mcp.*, wokelo_pricing.*, keye_pricing.*, termina_pricing.*, decile_pricing.*, nicrron_pricing.*, hacknation.*, tavily_hackathons.*, vendr_pitchbook*.*, diligence_assist.*. Duplicates: roundtable_alt.*, cb_insights_pricing_page.*, nfx_about.*, costbench_cbi_change.*. Not relevant: flux.*, hebbia.*, rogo.*, alphasense.*, dealum.*.
- docs/reports/20261022.02_research/raw/data_room/: R4 lists five empty, partial or duplicate saved pages under "Cleanup needed" at the end of research_data_room.md.
- docs/reports/20261022.02_research/raw/feasibility/: duplicate .html files that have a .txt beside them; hn/main.js; formd/2026q3_d.zip (not committed); frames_sample_head.json.
- data_room/hollis_voice_variant/, data_room/hollis_voice_variant_seed_drop/, data_room/answer_key_variant.json: smoke-test variant from the generator reviser (git-ignored); not for the blind demo, regenerate per data_room/SEALING.md.
- docs/reports/20261022.02_research/interviews.md.tmp (empty scratch file left by the orchestrator)
- docs/reports/20261022.02_research/interviews.md (retired: Ken chose online research only, 2026-10-22 1:34 PM)
- docs/reports/20261022.03_document_guides/raw/customer-references-and-letters-of-intent/labs_openviewpartners_com_customer_references_why_investors_need_them.txt (empty shell page)
- docs/reports/20261022.03_document_guides/raw/web_kjlabuz_substack_com_p_fast.txt; raw/founder-bios/hn_founder_lied_about_credentials_investors_found_out_diligence.json (empty); raw/founder-bios/justice_gov_usao_sdny_pr_founder_artificial_intelligence_start_charged_fraud.txt (empty); raw/ai-and-data-governance-documents/weil_com_media_mailings_2021_q2_ftc_orders_destruction_of_algorithms_created_from_unlawfully_acquire.txt and weil_ftc_orders_destruction_of_algorithms.pdf (unreadable); raw/hiring-plan-and-future-org/electricnoirstudios_notion_site_Hires_to_series_A_5f4cb196d22b4f7c9212d21ddfcbce5f.txt (empty). From the people-guides agent.
- docs/reports/20261022.03_document_guides/raw/ip-assignment/koleyjessen_com_media_publication_119_Important_Considerations_for_Portfolio_Company_Commercial_Cont.pdf (stray copy)
- docs/reports/20261022.03_document_guides/raw/*/hn_comment_*.json (search noise in the six financials folders); raw/bank-statements/ empty stubs: two justice.gov files and newsfilecorp_com_release_212484_SEC_Charges_Founder_of_AI_Hiring_Startup_Joonko_with_Fraud.txt

From the story-group guides agent, 2026-10-22 3:39 PM:

- docs/reports/20261022.03_document_guides/raw/hn-tmp/ (temporary Hacker News fetches)
- docs/reports/20261022.03_document_guides/raw/pitch-deck/hn_deck_*.json (temporary Hacker News fetches)
- `.who-am-i` (repo root, untracked): replaced by `.agent-owner` on 2026-10-24 to match the last hackathon.
- `docs/features/20261024.02_first_steps_ui/prototype/style` (symlink to docs/ongoing/style): replaced by the copy in `tc_style/` on 2026-10-24, because Lahe does not serve symlinks.
