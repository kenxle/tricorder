import json
root = "/Users/kennethstclair/Documents/workspace/tricorder/data_room/"
key = json.load(open(root + "answer_key.json"))
claims = json.load(open(root + "hollis_voice/01_overview/claims.json"))["claims"]
print("rows on the deck's claims page:", len(claims))
hit = {}
for f in key["flags"]:
    for loc in f["locations"]:
        if loc["file"].endswith("pitch_deck.pdf") and loc.get("page") == 14:
            hit.setdefault(loc.get("claims_row") or loc.get("text"), []).append(f["id"])
print("flags with a location on slide 14:", {k: v for k, v in hit.items()})
flagged_slides = sorted({loc["page"] for f in key["flags"] for loc in f["locations"] if loc["file"].endswith("pitch_deck.pdf") and loc.get("page") not in (None, 14)})
print("content slides carrying a planted flag:", flagged_slides)
print("deck claim rows that a planted flag names (by shown value):")
shown = {"ARR":"PF2","Clinics on Hollis":"PF7","Largest customer":"PF5","Gross margin":"PF6","Net revenue retention":"PF3","Runway":"PF4","Average monthly net burn, next 12 months":"PF4"}
n = 0
for c in claims:
    f = shown.get(c["label"])
    if f: n += 1
    print("  ", c["label"], c["value"], "slide", c["slide"], "->", f or "no flag")
print("claim rows tied to a flag:", n, "of", len(claims))
