"""Lay a Pandoc page out in the shape the house document style expects.

Pandoc writes plain HTML. The house style is written for a specific shape:
a title block (.hero), a links row (.toplinks), the contents folded shut
(.fold), then one numbered section (.sheet) per H2. It also styles callouts as
.insight panels and review verdicts as status dots. The functions here rewrite
Pandoc's output into that shape. They only run when a house style was found.

Older dossiers write callouts as ::: callout-* fenced divs. Those are mapped
onto the house components so old documents still render styled.
"""
import html as html_lib
import re

MARK_TITLE = ('<!-- forge:title -->', '<!-- /forge:title -->')
MARK_TOC = ('<!-- forge:toc -->', '<!-- /forge:toc -->')
MARK_BODY = ('<!-- forge:body -->', '<!-- /forge:body -->')

# The Pandoc template. It gives the page none of Pandoc's own styles. The
# build assembles <main> from the three marked pieces.
PAGE_TEMPLATE = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$pagetitle$</title>
$for(header-includes)$
$header-includes$
$endfor$
</head>
<body>
{MARK_TITLE[0]}$title${MARK_TITLE[1]}
{MARK_TOC[0]}$table-of-contents${MARK_TOC[1]}
{MARK_BODY[0]}
$body$
{MARK_BODY[1]}
</body>
</html>
"""

REVIEWS_DIVIDER = (
    '\n\n<hr class="reviews-divider">\n\n'
    '::: reviews-banner\n'
    'Review history: the full reviews for this document. They live in a '
    'separate `_reviews.md` file so agents can read the lean spec, and are '
    'merged here for review.\n'
    ':::\n\n'
)

# An authored links row. The source may carry one so a page served live has it;
# the build draws its own, linked to the built pages.
AUTHORED_TOPLINKS = re.compile(
    r'<nav\b[^>]*\bclass="toplinks"[^>]*>.*?</nav>[ \t]*\n?', re.S)


def _cut(html, marks):
    """Return (html without the marked piece, the piece)."""
    start = html.index(marks[0])
    end = html.index(marks[1], start)
    return html[:start] + html[end + len(marks[1]):], html[start + len(marks[0]):end]


def wrap_tables(html):
    """Wrap each table in the style's .scrollx, so a wide table scrolls on its
    own axis instead of widening the page. Pandoc does not nest tables, so a
    non-greedy match is safe."""
    return re.sub(r'(<table\b.*?</table>)',
                  r'<div class="scrollx">\1</div>',
                  html, flags=re.DOTALL)


def drop_rules_before_headings(html):
    """A Markdown `---` right before a heading would draw a hairline just above
    the heading's own room. The section break already does that job."""
    return re.sub(r"<hr\s*/?>\s*(?=<h2\b)", "", html)


def task_lists(html):
    """Give GFM task lists the shape Lahe's Markdown renderer writes: a
    class-free ul whose item holds the checkbox directly. The style's task-list
    rule is written for that shape; pandoc's ul.task-list with a <label> would
    otherwise show a browser bullet beside the box."""
    html = html.replace('<ul class="task-list">', "<ul>")
    return re.sub(r'<label>(<input type="checkbox"[^>]*?)\s*/?>(.*?)</label>',
                  lambda m: f'{m.group(1)} disabled="" /> {m.group(2)}',
                  html, flags=re.S)


# (insight classes, label). None means no tint: the label and the content
# only, as quiet labelled prose. A requirement is a spec fact, not a point to
# carry forward, so it does not get a panel.
CALLOUTS = {
    "req": (None, "Requirement"),
    "metric": ("insight", "Metrics"),
    "suggest": ("insight", "Suggestion"),
    "question": ("insight insight--caveat", "Open question"),
    "flag": ("insight insight--caveat", "Red flag"),
    "nongoal": (None, "Non-goals"),
}


_SECTION_TAG = re.compile(r"<section\b[^>]*>|</section\s*>")
_CALLOUT_SECTION = re.compile(r'<section(\s[^>]*\bclass="[^"]*\bcallout-[^"]*"[^>]*)>')


def callout_sections_to_divs(html):
    """Pandoc writes a fenced div that opens with a heading as a <section>.
    Turn each callout one back into a <div>, so it maps like any other
    callout and its heading stays inside it."""
    while True:
        m = _CALLOUT_SECTION.search(html)
        if not m:
            return html
        depth, close = 0, None
        for t in _SECTION_TAG.finditer(html, m.start()):
            depth += -1 if t.group(0).startswith("</") else 1
            if depth == 0:
                close = t
                break
        if close is None:
            return html
        html = (html[:m.start()] + f"<div{m.group(1)}>" + html[m.end():close.start()]
                + "</div>" + html[close.end():])


def map_callouts(html):
    """Map each ::: callout-* div onto the style system's insight panel.

    Metrics and suggestion take the accent panel. Open question and red flag
    take the caveat panel. Requirement and non-goals take no tint. The label
    rides on data-label, which the style draws for an insight panel; an
    author's own data-label wins. The untinted pair gets its label as the
    style's .eyebrow line, since nothing would draw it otherwise.

    The build never adds a bare `callout` class. In the style system that class
    is the solid ink block with white text.
    """
    def repl(m):
        attrs = m.group(1)
        cm = re.search(r'class="([^"]*)"', attrs)
        if not cm:
            return m.group(0)
        classes = cm.group(1).split()
        kind = next((c[len("callout-"):] for c in classes
                     if c.startswith("callout-") and c[len("callout-"):] in CALLOUTS), None)
        if kind is None:
            return m.group(0)
        base, label = CALLOUTS[kind]
        classes = [c for c in classes if c != "callout"]
        if base:
            classes = [c for c in base.split() if c not in classes] + classes
        new_attrs = attrs.replace(cm.group(0), f'class="{" ".join(classes)}"')
        lm = re.search(r'data-label="([^"]*)"', new_attrs)
        if lm:
            label = html_lib.unescape(lm.group(1))
        else:
            new_attrs += f' data-label="{html_lib.escape(label)}"'
        eyebrow = "" if base else f'\n<p class="eyebrow">{html_lib.escape(label)}</p>'
        return f"<div{new_attrs}>{eyebrow}"
    return re.sub(r"<div(\s[^>]*)>", repl, html)


_DIV_TAG = re.compile(r"<div\b[^>]*>|</div\s*>")


def _div_end(html, start):
    """Index just past the </div> that closes the <div> opening at start."""
    depth = 0
    for m in _DIV_TAG.finditer(html, start):
        depth += -1 if m.group(0).startswith("</") else 1
        if depth == 0:
            return m.end()
    return -1


_CALLOUT_OPEN = re.compile(r'<div(\s[^>]*\bclass="[^"]*\bcallout-(?:%s)\b[^"]*"[^>]*)>'
                           % "|".join(CALLOUTS))
_EYEBROW = re.compile(r'^\s*<p class="eyebrow">.*?</p>\s*', re.S)


def _callout_key(attrs):
    return (re.search(r'class="([^"]*)"', attrs).group(1),
            (re.search(r'data-label="([^"]*)"', attrs) or [None, None])[1])


def merge_callout_runs(html):
    """Merge a run of same-type callouts into one panel with one label.

    Twenty separate requirement panels read as decoration. A run is two or
    more callouts with the same classes and the same data-label and only
    whitespace between them; a heading or a paragraph between two callouts
    ends the run. The items' content follows one label, in order. A lone
    callout is left as it is.
    """
    out, pos = [], 0
    while True:
        m = _CALLOUT_OPEN.search(html, pos)
        if not m:
            out.append(html[pos:])
            return "".join(out)
        key = _callout_key(m.group(1))
        end = _div_end(html, m.start())
        if end == -1:
            out.append(html[pos:])
            return "".join(out)
        items = [(m.group(1), html[m.end():end - len("</div>")])]
        while True:
            gap = len(html[end:]) - len(html[end:].lstrip())
            nxt = _CALLOUT_OPEN.match(html, end + gap)
            if not nxt or _callout_key(nxt.group(1)) != key:
                break
            nend = _div_end(html, nxt.start())
            if nend == -1:
                break
            items.append((nxt.group(1), html[nxt.end():nend - len("</div>")]))
            end = nend
        out.append(html[pos:m.start()])
        if len(items) == 1:
            out.append(html[m.start():end])
        else:
            first_attrs = re.sub(r'\sid="[^"]*"', "", items[0][0])
            parts = []
            for i, (item_attrs, inner) in enumerate(items):
                if i:
                    inner = _EYEBROW.sub("", inner, count=1)
                idm = re.search(r'\sid="([^"]*)"', item_attrs)
                anchor = f'<span id="{idm.group(1)}"></span>' if idm else ""
                parts.append(anchor + inner.strip())
            out.append(f"<div{first_attrs}>\n" + "\n".join(parts) + "\n</div>")
        pos = end


# Verdict word -> the style's status-dot colour.
VERDICT_DOTS = {"Accepted": "sage", "Rejected": "purple", "Deferred": "faint"}


def unwrap_plain_callouts(html):
    """Requirement and non-goals read as plain labelled prose: their wrapper div
    goes, leaving the .eyebrow label and the content as ordinary blocks. The
    eyebrow carries its own room above it, so a label after a previous callout
    never sits flush against it, which a wrapper div would cause (its last
    paragraph drops its bottom margin)."""
    out, pos = [], 0
    while True:
        m = _CALLOUT_OPEN.search(html, pos)
        if not m:
            out.append(html[pos:])
            return "".join(out)
        end = _div_end(html, m.start())
        attrs = m.group(1)
        if end == -1 or re.search(r'\binsight\b', attrs):
            out.append(html[pos:m.end()])
            pos = m.end()
            continue
        inner = html[m.end():end - len("</div>")].strip()
        idm = re.search(r'\sid="([^"]*)"', attrs)
        if idm:
            inner = inner.replace('<p class="eyebrow">',
                                  f'<p class="eyebrow" id="{idm.group(1)}">', 1)
        out.append(html[pos:m.start()] + inner)
        pos = end


def colorize_dispositions(html):
    """Mark Accepted/Rejected/Deferred in disposition-table cells with the
    style's status dot."""
    return re.sub(
        r'(<td[^>]*>)\s*(Accepted|Rejected|Deferred)\s*(</td>)',
        lambda m: (f'{m.group(1)}<span class="status-dot status-dot--'
                   f'{VERDICT_DOTS[m.group(2)]}">{m.group(2)}</span>{m.group(3)}'),
        html,
    )


# Finding identifiers used in disposition tables and review prose (RF1, S2, C1,
# Q3, K1, ...). The `#` column of a disposition table links down to the matching
# verbatim entry in the merged reviews so the human can jump spec → detail.
_FINDING = r'(?:RF|S|C|Q|K)\d+'


def _persona_key(heading_html):
    """Normalize a review heading to a persona slug so a disposition table and
    its verbatim prose resolve to the same anchor namespace. 'Architect Review'
    and 'Architect Review (Round 1)' both -> 'architect'."""
    t = re.sub(r"<[^>]+>", "", heading_html).lower().replace("’", "'")
    t = re.sub(r"\(round[^)]*\)", "", t)
    t = re.sub(r"review\s*$", "", t.strip())
    return re.sub(r"[^a-z0-9]+", "-", t.strip().strip("'").strip()).strip("-")


def crosslink_findings(html):
    """Two passes over the merged HTML, persona-scoped so RF1-in-Architect and
    RF1-in-Security don't collide:
      1. Anchor every `<strong>RF1: ...` finding marker in the review prose
         with id `{persona}-rf1`.
      2. Turn each disposition-table `#`-column cell (`<td>RF1</td>`) into a link
         to that anchor, when it exists.
    """
    parts = re.split(r"(<h2\b[^>]*>.*?</h2>)", html, flags=re.S)
    anchors = set()

    persona = None
    for i, part in enumerate(parts):
        if i % 2 == 1:
            persona = _persona_key(part)
            continue
        if not persona:
            continue

        def _anchor(m, p=persona):
            aid = f"{p}-{m.group(1).lower()}"
            anchors.add(aid)
            return f'<span id="{aid}" class="finding-anchor"></span>{m.group(0)}'

        parts[i] = re.sub(rf"<strong>({_FINDING})\b", _anchor, part)

    persona = None
    for i, part in enumerate(parts):
        if i % 2 == 1:
            persona = _persona_key(part)
            continue
        if not persona:
            continue

        def _link(m, p=persona):
            aid = f"{p}-{m.group(2).lower()}"
            if aid in anchors:
                return f'{m.group(1)}<a href="#{aid}">{m.group(2)}</a>{m.group(3)}'
            return m.group(0)

        parts[i] = re.sub(rf"(<td[^>]*>)({_FINDING})(</td>)", _link, part)

    return "".join(parts)


SECTION_NUM_RE = re.compile(
    r'^(\s*(?:<(?:i|svg)\b[^>]*>(?:</(?:i|svg)>)?\s*)?)(\d{1,2})[.)]\s+')


# Block containers an <h2> can sit inside. Only an <h2> outside all of them
# opens a section; one inside a callout, a list item or a quote stays put.
_CONTAINER = re.compile(
    r"<(/?)(div|section|details|blockquote|aside|figure|nav|ul|ol|li|table)\b[^>]*>",
    re.I)
_H2 = re.compile(r"<h2([^>]*)>(.*?)</h2>", re.S)


def top_level_h2s(body):
    """Yield the match of each <h2> that is not inside a block container."""
    depth, pos = 0, 0
    while True:
        h = _H2.search(body, pos)
        if not h:
            return
        for c in _CONTAINER.finditer(body, pos, h.start()):
            depth = max(0, depth + (-1 if c.group(1) else 1))
        if depth == 0:
            yield h
        pos = h.end()


def wrap_sections(body):
    """The numbered sections. Each <h2> becomes the
    style's hanging-rule head row with "Section N" on the right, and the head
    row plus everything up to the next one is wrapped in <section class="sheet">.

    A heading that already leads with a number ("## 2. Method") gives that
    number to the label and drops it from the heading text; headings without
    one continue the count.
    """
    state = {"n": 0}

    def repl(m):
        attrs, inner = m.group(1), m.group(2)
        num = SECTION_NUM_RE.match(inner)
        if num:
            state["n"] = int(num.group(2))
            inner = num.group(1) + inner[num.end():]
        else:
            state["n"] += 1
        return (f'<div class="sheet-head"><h2{attrs}>{inner}</h2>'
                f'<span class="n">Section {state["n"]}</span></div>')

    heads = list(top_level_h2s(body))
    if not heads:
        return body
    out = [body[:heads[0].start()]]
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(body)
        piece = repl(h) + body[h.end():end]
        out.append(f'<section class="sheet">\n{piece.strip()}\n</section>\n')
    return "".join(out)


def contents_fold(toc):
    """Pandoc's contents list inside the style's folded section, open."""
    if "<li" not in toc:
        return ""
    return ('<details class="fold contents" open>'
            '<summary class="fold-head"><span class="fold-arrow" aria-hidden="true"></span>'
            '<h2>Contents</h2></summary>'
            '<div class="fold-body">'
            f'<nav id="TOC" class="contents-list">\n{toc.strip()}\n</nav>'
            '</div></details>')


def split_preamble(body):
    """Return (what comes before the first top-level <h2>, the rest)."""
    first = next(top_level_h2s(body), None)
    if first is None:
        return body.strip(), ""
    return body[:first.start()].strip(), body[first.start():]


def hero(title, preamble):
    """The title block: the title, then the text before the first
    section, its first paragraph promoted to the lede."""
    if preamble.startswith("<p>"):
        preamble = '<p class="lede">' + preamble[len("<p>"):]
    return f'<div class="hero">\n<h1>{title}</h1>\n{preamble}\n</div>'


def assemble(head, html, nav):
    """Turn pandoc's output into the page: <main> holding the title block, the
    links row, the contents fold, and the body in sheets. head is everything
    before <body>; html is <body> onward.

    The title and the text before the first section become the hero, its
    first paragraph the lede. Each H2 then opens its own numbered section.
    """
    html, title = _cut(html, MARK_TITLE)
    html, toc = _cut(html, MARK_TOC)
    html, body = _cut(html, MARK_BODY)
    preamble, rest = split_preamble(body)
    parts = [hero(title.strip(), preamble), nav, contents_fold(toc), wrap_sections(rest)]
    main = ('<main data-container="Feature document">\n'
            + "\n".join(p for p in parts if p) + "\n</main>")
    idx = html.index("<body>") + len("<body>")
    return head + html[:idx] + "\n" + main + html[idx:]


def nav_bar(current, labels):
    """The links row: the style's .toplinks component. labels is a list of
    (key, label, href). The current page is a span with aria-current."""
    items = []
    for key, label, href in labels:
        text = html_lib.escape(label)
        if key == current:
            items.append(f'<span aria-current="page">{text}</span>')
        else:
            items.append(f'<a href="{html_lib.escape(href, quote=True)}">{text}</a>')
    return ('<nav class="toplinks" aria-label="Documents">'
            '<span class="toplinks-label">Docs</span>' + ''.join(items) + '</nav>')


def split_title(md):
    """Pull the first ATX H1 out of the Markdown; return (title, body)."""
    lines = md.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.startswith('# '):
            del lines[i]
            return line[2:].strip(), ''.join(lines).lstrip('\n')
    return '', md


def rewrite_body(html):
    """Every rewrite pattern-matches HTML, so run this on the body only. The
    style goes into the head afterwards, where no pattern can match its text."""
    html = wrap_tables(html)
    html = drop_rules_before_headings(html)
    html = task_lists(html)
    html = callout_sections_to_divs(html)
    html = map_callouts(html)
    html = merge_callout_runs(html)
    html = unwrap_plain_callouts(html)
    html = colorize_dispositions(html)
    return crosslink_findings(html)
