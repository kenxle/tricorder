"""Arithmetic for research_landscape.md. Every figure typed into the report comes from here.

Inputs are prices read on each vendor's own page (files under raw/landscape/):
  Dealroom      dealroom_pricing.txt        EUR 250 and EUR 325 per seat per month, billed annually, 3 seat minimum
  Crunchbase    chrome_pages_pricing.txt    Pro $49 per month (annual) or $99 (monthly); Business from $199 (annual)
  Affinity      affinity_pricing.txt        $2,000 / $2,300 / $2,700 per user per year
  Akta          akta_pricing.txt            credit cost $0.05 pay as you go, $0.04 subscription; per-call credits
  Akta          chrome_pages_pricing.txt    Subscription $50 per month for 1,250 credits; Enterprise from $2,000 per month
  You.com       youcom_api.txt              $5 per 1,000 calls, $100 free credits
  Tavily        tavily_pricing.txt          $0.008 per credit pay as you go; Project $30 per month for 4,000 credits

Run: python3 -I landscape_price_math.py
"""

print("DEALROOM (EUR, annual)")
for name, per_month in (("Premium", 250), ("Premium Plus", 325)):
    print("  %-13s 3 seats %6d   10 seats %6d" % (name, per_month * 12 * 3, per_month * 12 * 10))

print("\nCRUNCHBASE (USD per year, one user)")
print("  Pro annual   %d" % (49 * 12))
print("  Pro monthly  %d" % (99 * 12))
print("  Business     from %d (annual billing)" % (199 * 12))

print("\nAFFINITY (USD per year, 5 users)")
for name, per_user in (("Essential", 2000), ("Scale", 2300), ("Advanced", 2700)):
    print("  %-10s %6d" % (name, per_user * 5))

print("\nAKTA")
sub_per_credit = 50 / 1250
print("  Subscription credit cost: %.2f dollars (page says 0.04)" % sub_per_credit)
print("  Enterprise from: %d dollars per year" % (2000 * 12))
# One company, the signals a first-pass readout would pull. Credits from docs.akta.pro pricing.md.
sections = {"firmographic": 2, "business_model": 2, "financial_estimate": 0.5, "management_profile": 1,
            "strategic_signal": 1.5, "customer_profile": 1}
news = 0.1 + 0.01 * 20          # one news_signals call returning 20 articles
alt = {"headcount_trends": 2.5, "website_traffic": 1.5, "job_posts_10_records": 4,
       "product_reviews_50": 1.5, "employee_reviews_50": 1.5}
company_profile = sum(sections.values())
signal_pull = news + sum(alt.values())
one_company = company_profile + signal_pull
print("  company profile sections: %.2f credits" % company_profile)
print("  news (1 call, 20 articles) plus 5 alt-signal calls: %.2f credits" % signal_pull)
print("  one company, everything above: %.2f credits = %.2f dollars at 0.04, %.2f at 0.05" % (
    one_company, one_company * 0.04, one_company * 0.05))
five = one_company * 5
print("  target plus 4 competitors: %.2f credits = %.2f dollars at 0.04" % (five, five * 0.04))
print("  one month of Subscription (1,250 credits) covers %.0f companies pulled this way" % (1250 / one_company))
print("  (alt-signal calls need the Subscription plan or higher per docs.akta.pro/getting-started/rate-limits)")

print("\nYOU.COM")
print("  $100 free credits at $5 per 1,000 calls = %d calls" % (100 / 5 * 1000))

print("\nTAVILY")
print("  1,000 credits at $0.008 = %.2f dollars" % (1000 * 0.008))
print("  Project plan: $30 for 4,000 credits = %.4f dollars per credit" % (30 / 4000))
