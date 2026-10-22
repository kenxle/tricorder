import json, subprocess, re, pathlib
root = pathlib.Path("/Users/kennethstclair/Documents/workspace/tricorder/data_room")
key = json.load(open(root/"answer_key.json"))
txt = subprocess.run(["pdftotext","-layout",str(root/"hollis_voice/00_welcome/cover_note_and_index.pdf"),"-"],capture_output=True,text=True).stdout
flat = re.sub(r"\s+","",txt)
listed=[]; missing=[]
for f in key["full_room_files"]:
    ok = re.sub(r"\s+","",f) in flat
    (listed if ok else missing).append(f)
print("files in room:", len(key["full_room_files"]))
print("named in the index text (whitespace ignored):", len(listed))
print("not named:", missing)
tier_first = len(re.findall(r"First tier", txt)); tier_second = len(re.findall(r"Second tier", txt))
print("first-tier rows:", tier_first, "second-tier rows:", tier_second)
print("seed drop files:", len(key["seed_drop_files"]))
rows = [l for l in txt.splitlines() if re.match(r"\s*\d+\s+\S+/\S+", l)]
print("rows that start with a number then a path:", len(rows))
split = [l for l in txt.splitlines() if re.match(r"^\s*1\s{2,}\S", l)]
print("lines beginning with a lone 1 and a space gap:", len(split))
for w in ["raise","$9,000,000","hello@","@","phone","valuation"]:
    print(repr(w), w in txt)
