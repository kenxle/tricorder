"""Contrast check for the Tricorder style tokens.

Reads the colour tokens from tricorder.css (beside this file), so the numbers always match the stylesheet.
Prints a Markdown table of every text pairing the guide uses, in dark and light, with its WCAG 2 contrast ratio.
Fails (exit 1) if any text pairing is under 4.5:1, if the focus ring is under 3:1 against the ground,
or if the two copies of the light tokens (prefers-color-scheme and [data-theme="light"]) differ.

Run: python3 docs/ongoing/style/check_contrast.py
"""
import re
import sys
from pathlib import Path

CSS = Path(__file__).resolve().parent / "tricorder.css"


def block(css, selector_regex):
    m = re.search(selector_regex + r"\s*\{([^{}]*)\}", css)
    if not m:
        sys.exit(f"could not find the block {selector_regex}")
    return dict(re.findall(r"--(tc-[\w-]+):\s*([^;]+);", m.group(1)))


def parse(value):
    value = value.strip()
    m = re.fullmatch(r"#([0-9a-fA-F]{6})", value)
    if m:
        h = m.group(1)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (1.0,)
    m = re.fullmatch(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)", value)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)), float(m.group(4)))
    return None


def over(top, bottom):
    """Composite a colour with alpha over an opaque colour."""
    a = top[3]
    return tuple(round(top[i] * a + bottom[i] * (1 - a)) for i in range(3)) + (1.0,)


def luminance(c):
    def ch(v):
        v = v / 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in c[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg, bg):
    l1, l2 = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def hexof(c):
    return "#%02x%02x%02x" % c[:3]


# Text pairings: (what, foreground token, background token, optional tint laid over the background).
TEXT = [
    ("Headings, figures", "tc-ink", "tc-ground", None),
    ("Body copy", "tc-ink-2", "tc-ground", None),
    ("Labels, axes, help", "tc-ink-3", "tc-ground", None),
    ("Labels on a hover fill", "tc-ink-3", "tc-surface-2", None),
    ("Body copy on a panel", "tc-ink-2", "tc-surface", None),
    ("Metal label (Ask the founder, band label)", "tc-accent", "tc-ground", None),
    ("Metal label on a panel", "tc-accent", "tc-surface", None),
    ("Link hover", "tc-accent", "tc-ground", None),
    ("Primary button", "tc-btn-fg", "tc-btn-bg", None),
    ("Primary button, hover", "tc-btn-fg", "tc-btn-bg-hover", None),
    ("Secondary button, hover", "tc-ink", "tc-surface-2", None),
    ("Disabled button", "tc-ink-3", "tc-ground", None),
    ("Looking strong mark", "tc-strong", "tc-surface", "tc-strong-bg"),
    ("Looking weak mark", "tc-weak", "tc-surface", "tc-weak-bg"),
    ("Mixed mark", "tc-mixed", "tc-surface", "tc-mixed-bg"),
    ("Not enough in the room mark", "tc-thin", "tc-surface", "tc-thin-bg"),
    ("Out-of-band figure", "tc-weak", "tc-surface", None),
    ("Source chip", "tc-ink-2", "tc-surface", None),
    ("Source chip, hover", "tc-ink", "tc-surface-2", None),
]
# Non-text: a focus ring needs 3:1 against what it sits on (WCAG 1.4.11). Hairlines are reported, not judged.
FOCUS = [("Focus ring", "tc-accent", "tc-ground"), ("Focus ring on a panel", "tc-accent", "tc-surface")]
INFO = [("Input and chip border (rule-2)", "tc-rule-2", "tc-ground"), ("Hairline (rule)", "tc-rule", "tc-ground"),
        ("Band edge (Ask the founder outline)", "tc-band-edge", "tc-ground")]


def main():
    css = CSS.read_text()
    dark = block(css, r":root,\s*\.tc-dark")
    light_media = block(css, r':root:not\(\[data-theme="dark"\]\)')
    light = block(css, r':root\[data-theme="light"\]')
    failed = []
    if light_media != light:
        diff = sorted(k for k in set(light) | set(light_media) if light.get(k) != light_media.get(k))
        failed.append("light tokens differ between the media query and [data-theme=light]: " + ", ".join(diff))

    print("| Pairing | Theme | Text | On | Ratio | Floor | Result |")
    print("|---|---|---|---|---|---|---|")
    for theme, t in (("Dark", dark), ("Light", light)):
        for what, fg, bg, tint in TEXT:
            b = parse(t[bg])
            if tint:
                b = over(parse(t[tint]), b)
            r = ratio(parse(t[fg]), b)
            ok = r >= 4.5
            on = f"`{bg}`" + (f" + `{tint}`" if tint else "")
            print(f"| {what} | {theme} | `{fg}` {t[fg]} | {on} {hexof(b)} | {r:.1f}:1 | 4.5:1 | {'pass' if ok else 'FAIL'} |")
            if not ok:
                failed.append(f"{theme}: {what} {r:.2f}:1")
        for what, fg, bg in FOCUS:
            r = ratio(parse(t[fg]), parse(t[bg]))
            ok = r >= 3
            print(f"| {what} | {theme} | `{fg}` {t[fg]} | `{bg}` {t[bg]} | {r:.1f}:1 | 3:1 | {'pass' if ok else 'FAIL'} |")
            if not ok:
                failed.append(f"{theme}: {what} {r:.2f}:1")
        for what, fg, bg in INFO:
            r = ratio(parse(t[fg]), parse(t[bg]))
            print(f"| {what} | {theme} | `{fg}` {t[fg]} | `{bg}` {t[bg]} | {r:.1f}:1 | none | info |")

    if failed:
        print("\nFAILED:\n" + "\n".join(failed))
        sys.exit(1)
    print("\nAll text pairings meet 4.5:1 and the focus ring meets 3:1 in both themes.")


if __name__ == "__main__":
    main()
