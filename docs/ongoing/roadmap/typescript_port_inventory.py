import subprocess, collections, csv, sys
files = subprocess.run(["git","ls-files"],capture_output=True,text=True).stdout.split()
rows = collections.defaultdict(lambda: [0,0,0,0])
for f in files:
    top = f.split("/")[0] if "/" in f else "(root)"
    if top in ("docs","data_room",".claude",".github"): continue
    ext = f.rsplit(".",1)[-1] if "." in f else ""
    if ext not in ("py","ts","tsx"): continue
    try: n = sum(1 for _ in open(f,encoding="utf-8"))
    except Exception: continue
    test = "/tests/" in f or f.split("/")[-1].startswith("test_") or ".test." in f
    i = (0 if ext=="py" else 2) + (1 if test else 0)
    rows[top][i] += n
w = csv.writer(sys.stdout)
w.writerow(["folder","py_lines","py_test_lines","ts_lines","ts_test_lines"])
tot=[0,0,0,0]
for k in sorted(rows):
    w.writerow([k]+rows[k]); tot=[a+b for a,b in zip(tot,rows[k])]
w.writerow(["TOTAL"]+tot)
