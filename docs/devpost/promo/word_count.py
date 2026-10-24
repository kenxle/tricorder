# Counts the voiceover words per line and in total, from LINES in vo.py.
from vo import LINES

total = 0
for name, start, maxlen, speed, text in LINES:
    n = len(text.split())
    total += n
    print(f"{name}\t{n}\t{text}")
print("total", total)
