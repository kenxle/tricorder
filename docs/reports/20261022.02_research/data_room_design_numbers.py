"""Design numbers for the synthetic data room (R4, research_data_room.md Part 3).

This is a design check, not the generator. It simulates the fictional company once, with a
fixed seed, and computes the TRUE value and the SHOWN value for each planted flag, so the
numbers quoted in research_data_room.md come from a script and are consistent with each other.
The real generator (data_room/generate.py, to be written) reuses this logic and writes the files.

Fictional company (placeholder name, check it against a name search before use):
  Hollis Voice, an AI phone agent for independent veterinary clinics, New York.
  Data as of 2026-09-30. Series A ask: 9,000,000.

Run: python3 -I data_room_design_numbers.py
Writes: data_room_design_numbers.json (the answer-key preview) next to this file.
"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20261024  # the hackathon date, so the run is reproducible and easy to remember

N_MONTHS = 21  # 2025-01 .. 2026-09
MONTH_LABELS = [f"{2025 + (m // 12)}-{(m % 12) + 1:02d}" for m in range(N_MONTHS)]
PLAN_PRICE = {"Starter": 349, "Standard": 649, "Pro": 1099}
PLAN_ORDER = ["Starter", "Standard", "Pro"]

# Churn chance per month by months since first invoice (tenure 1 is the first month)
def churn_p(tenure):
    if tenure <= 2:
        return 0.09
    if tenure <= 12:
        return 0.012
    return 0.01

UPGRADE_P = 0.04          # monthly chance a customer moves up one plan
ONBOARDING_FEE = 500       # one-time, never counted in ARR (a clean case, not a planted flag)

# Named customers (fictional)
BIG = {"name": "Cedar & Pine Animal Hospitals", "start": 10, "mrr_start": 18000,
       "expand_at": 15, "mrr_after": 36000}
PILOT = {"name": "Marlow Veterinary Group", "monthly_fee": 15000, "months": 6,
         "start": 19, "termination_days": 30}  # signed 2026-08, a pilot, not a subscription


def simulate(rng):
    customers = []  # each: dict(id, start, plan, churn_month or None, mrr_by_month list)
    cid = 0
    for m in range(N_MONTHS):
        n_new = max(2, round(5 + 0.7 * m + rng.uniform(-1.5, 1.5)))
        for _ in range(n_new):
            cid += 1
            plan = rng.choices(PLAN_ORDER, weights=[45, 40, 15])[0]
            customers.append({"id": f"C{cid:04d}", "start": m, "plan": plan, "mrr": [0] * N_MONTHS,
                              "churn": None, "kind": "standard", "first_plan": plan})
    # play each customer forward
    for c in customers:
        plan = c["plan"]
        alive = True
        for m in range(c["start"], N_MONTHS):
            tenure = m - c["start"] + 1
            if m > c["start"]:
                if rng.random() < churn_p(tenure):
                    c["churn"] = m
                    alive = False
                    break
                if rng.random() < UPGRADE_P and PLAN_ORDER.index(plan) < 2:
                    plan = PLAN_ORDER[PLAN_ORDER.index(plan) + 1]
            c["mrr"][m] = PLAN_PRICE[plan]
        c["plan"] = plan
    # the big customer
    big = {"id": "C-BIG", "start": BIG["start"], "plan": "Group", "mrr": [0] * N_MONTHS,
           "churn": None, "kind": "big", "first_plan": "Group"}
    for m in range(BIG["start"], N_MONTHS):
        big["mrr"][m] = BIG["mrr_start"] if m < BIG["expand_at"] else BIG["mrr_after"]
    customers.append(big)
    return customers


def main():
    rng = random.Random(SEED)
    customers = simulate(rng)
    last = N_MONTHS - 1

    mrr_total = [sum(c["mrr"][m] for c in customers) for m in range(N_MONTHS)]
    paying = [sum(1 for c in customers if c["mrr"][m] > 0) for m in range(N_MONTHS)]
    ever = len(customers)

    true_mrr = mrr_total[last]
    true_arr = 12 * true_mrr
    pilot_arr_shown = 12 * PILOT["monthly_fee"]
    model_arr = true_arr + pilot_arr_shown

    # Deck and video numbers are authored claims, rounded the way a founder rounds.
    deck_arr = math.ceil(model_arr * 1.10 / 100_000) * 100_000
    video_arr = math.ceil((deck_arr + 250_000) / 500_000) * 500_000

    # --- Revenue and gross margin
    onboarding_last = sum(ONBOARDING_FEE for c in customers if c["start"] == last)
    pilot_rev_last = PILOT["monthly_fee"]
    revenue_last = true_mrr + onboarding_last + pilot_rev_last
    sub_rev_basis = true_mrr + pilot_rev_last
    telephony_pct, licences_pct = 0.15, 0.05      # in COGS in the shown P&L
    infra_pct = 0.11                              # cloud hosting + model inference, shown under R&D
    support_fte, support_base, load = 2, 95_000, 1.28
    support_cost = support_fte * support_base * load / 12   # shown under S&M
    cogs_shown = sub_rev_basis * (telephony_pct + licences_pct)
    cogs_true = cogs_shown + sub_rev_basis * infra_pct + support_cost
    gm_shown = 1 - cogs_shown / sub_rev_basis
    gm_true = 1 - cogs_true / sub_rev_basis

    # --- Concentration
    big_share_true = BIG["mrr_after"] / true_mrr
    claimed_top_customer_share = 0.09
    mrrs = sorted((c["mrr"][last] for c in customers if c["mrr"][last] > 0), reverse=True)
    top3_share = sum(mrrs[:3]) / true_mrr

    # --- Cohorts (month-12 retention for cohorts that have 12 months of data: starts 0..8)
    rows = []
    for start in range(0, last - 11):
        cohort = [c for c in customers if c["start"] == start and c["kind"] == "standard"]
        start_mrr = sum(c["mrr"][start] for c in cohort)
        end_m = start + 12
        end_mrr = sum(c["mrr"][end_m] for c in cohort)
        capped = sum(min(c["mrr"][end_m], c["mrr"][start]) for c in cohort)
        early_churn = [c for c in cohort if c["churn"] is not None and c["churn"] - c["start"] <= 2]
        kept = [c for c in cohort if c not in early_churn]
        kept_start = sum(c["mrr"][start] for c in kept)
        kept_end = sum(c["mrr"][end_m] for c in kept)
        rows.append({"cohort": MONTH_LABELS[start], "customers": len(cohort), "early_churners": len(early_churn),
                     "start_mrr": start_mrr, "end_mrr": end_mrr, "capped_end": capped,
                     "reported_start": kept_start, "reported_end": kept_end})
    ts = sum(r["start_mrr"] for r in rows)
    nrr_true = sum(r["end_mrr"] for r in rows) / ts
    grr_true = sum(r["capped_end"] for r in rows) / ts
    nrr_reported = sum(r["reported_end"] for r in rows) / sum(r["reported_start"] for r in rows)
    logos_true = sum(r["customers"] for r in rows)
    logos_reported = logos_true - sum(r["early_churners"] for r in rows)

    # --- Vanity metric: cumulative accounts created presented as active clinics
    trial_conversion = 0.70
    accounts_created_cum = round(ever / trial_conversion)
    paying_now = paying[last]

    # --- Burn versus hiring plan (forward 30 months from 2026-10, Series A of 9,000,000 lands 2027-01)
    cash_start = 1_800_000
    series_a, series_a_month = 9_000_000, 3     # month index 3 = 2027-01
    headcount_now, base_now = 17, 140_000
    payroll_now = headcount_now * base_now * load / 12
    other_opex_now = 0.11 * sub_rev_basis + 60_000   # infra (counted again here only as cash) + rent, tools, legal
    # revenue growth assumption: use trailing 6 month compound monthly growth, capped
    g = (mrr_total[last] / mrr_total[last - 6]) ** (1 / 6) - 1
    g_used = 0.035  # a flat planning assumption, below the observed trailing growth
    planned_hires = 24
    modeled_hires = 8
    hire_base = 165_000
    # hires start evenly across the 12 months from 2026-10 (two per month); the model counts only the first 8
    def runway(hires_counted):
        cash = cash_start
        rev = sub_rev_basis
        hc_cost = payroll_now
        months = 0
        burns = []
        for t in range(1, 61):
            for k in range(1, hires_counted + 1):
                if math.ceil(k * 12 / planned_hires) == t:
                    hc_cost += hire_base * load / 12
            rev *= (1 + g_used)
            cogs = rev * (telephony_pct + licences_pct)
            program = 140_000 if t > series_a_month else 0   # sales and marketing programs funded by the round
            burn = hc_cost + other_opex_now + program + cogs - rev
            if t == series_a_month + 1:
                cash += series_a
            cash -= burn
            burns.append(burn)
            if cash <= 0:
                return t - 1, burns
            months = t
        return months, burns
    runway_shown, burns_shown = runway(modeled_hires)
    runway_true, burns_true = runway(planned_hires)
    avg_burn_shown = sum(burns_shown[:12]) / 12
    avg_burn_true = sum(burns_true[:12]) / 12

    safe_amount, safe_cap = 2_000_000, 12_000_000
    a_pre = 45_000_000
    out = {
        "safe_amount": safe_amount,
        "safe_post_money_cap": safe_cap,
        "safe_ownership_before_series_a": round(safe_amount / safe_cap, 4),
        "series_a_raise": series_a,
        "series_a_pre_money": a_pre,
        "series_a_post_money": a_pre + series_a,
        "series_a_ownership": round(series_a / (a_pre + series_a), 4),
        "cash_at_as_of_date": cash_start,
        "headcount_now": headcount_now,
        "headcount_after_hiring_plan": headcount_now + planned_hires,
        "seed": SEED,
        "as_of": "2026-09-30",
        "company_placeholder": "Hollis Voice",
        "months": N_MONTHS,
        "customers_ever_paying": ever,
        "paying_clinics_now": paying_now,
        "mrr_true": true_mrr,
        "arr_true_recurring": true_arr,
        "arr_model_shown": model_arr,
        "arr_deck_shown": deck_arr,
        "arr_video_spoken": video_arr,
        "pilot_fee_per_month": PILOT["monthly_fee"],
        "pilot_arr_counted": pilot_arr_shown,
        "pilot_fees_actually_contracted": PILOT["monthly_fee"] * PILOT["months"],
        "big_customer_share_true": round(big_share_true, 3),
        "big_customer_share_claimed_under": claimed_top_customer_share,
        "top3_share_true": round(top3_share, 3),
        "gross_margin_shown": round(gm_shown, 3),
        "gross_margin_true": round(gm_true, 3),
        "nrr_12m_true": round(nrr_true, 3),
        "grr_12m_true": round(grr_true, 3),
        "nrr_12m_reported_in_cohort_tab": round(nrr_reported, 3),
        "cohort_customers_true": logos_true,
        "cohort_customers_reported": logos_reported,
        "cohorts_with_12m_data": len(rows),
        "accounts_created_cumulative_shown_as_active": accounts_created_cum,
        "paying_clinics_true": paying_now,
        "runway_months_shown_in_model": runway_shown,
        "runway_months_implied_by_hiring_plan": runway_true,
        "avg_monthly_net_burn_first_12m_shown": round(avg_burn_shown),
        "avg_monthly_net_burn_first_12m_implied": round(avg_burn_true),
        "hires_in_hiring_plan": planned_hires,
        "hires_counted_in_model": modeled_hires,
        "revenue_growth_used_per_month": round(g_used, 3),
        "revenue_growth_trailing_6m_observed": round(g, 3),
    }
    with open(os.path.join(HERE, "data_room_design_numbers.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    for k, v in out.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
