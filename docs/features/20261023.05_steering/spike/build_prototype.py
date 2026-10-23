"""Write 02_prototype/prototype.html from the template and spike/out/spike.json.

    python3 docs/features/20261023.05_steering/spike/build_prototype.py
"""

from pathlib import Path

HERE = Path(__file__).parent
spike = (HERE / "out" / "spike.json").read_text(encoding="utf-8")
html = (HERE / "prototype_template.html").read_text(encoding="utf-8").replace("/*SPIKE*/null", spike.strip())
target = HERE.parent / "02_prototype" / "prototype.html"
target.write_text(html, encoding="utf-8")
print(f"wrote {target}")
