#!/usr/bin/env python3
"""Compose trusted Markdown dossiers into offline HTML using external Pandoc.

When the house document style is found (see doc_style.py), each page inlines it
and uses its layout. Otherwise the pages use a small plain stylesheet and the
build prints one line to stderr saying so. Neither path uses the network.
"""
import argparse
import html
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
import doc_layout
import doc_style
import doc_diagrams

INCLUDE = re.compile(r'<!--\s*forge-include:\s*([^>]+?)\s*-->')
ASSETS = Path(__file__).resolve().parents[1] / 'assets'
HEADER = ASSETS / 'header.html'
HOUSE_HEADER = ASSETS / 'house_header.html'
STYLE_MARKER = '<!-- FORGE_DOC_STYLE -->'

def expand(path, root, stack=()):
    path, root = Path(path).resolve(), Path(root).resolve()
    if not path.is_relative_to(root):
        raise ValueError('Include escapes dossier: ' + str(path))
    if path in stack:
        raise ValueError('Include cycle: ' + str(path))
    def replace(match):
        return expand(path.parent / match.group(1).strip(), root, stack + (path,))
    return INCLUDE.sub(replace, path.read_text(encoding='utf-8'))

def label_for(stem, stems):
    """A short label for the links row: the word after the number, when that
    word is unique among the pages, else the whole file name."""
    def word(name):
        return name.split('_')[1] if '_' in name else name
    if [word(t) for t in stems].count(word(stem)) > 1:
        return stem
    return word(stem).replace('-', ' ').capitalize()


def run_pandoc_house(title, body, header_text):
    """Render with the house page template. The page layout is assembled later."""
    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)
        template, header = temp / 'page.html', temp / 'header.html'
        template.write_text(doc_layout.PAGE_TEMPLATE, encoding='utf-8')
        header.write_text(header_text, encoding='utf-8')
        command = ['pandoc', '--from', 'gfm+fenced_divs+yaml_metadata_block',
                   '--to', 'html5', '--standalone', '--toc', '--toc-depth=3',
                   '--template', str(template), '--include-in-header', str(header),
                   '--metadata', 'title=' + (title or 'Untitled')]
        # The house style draws code in one ink; Pandoc's highlighter would add
        # its own palette. The flag name changed between Pandoc versions.
        try:
            result = subprocess.run(command + ['--syntax-highlighting=none'],
                                    input=body, text=True, capture_output=True, check=True)
        except subprocess.CalledProcessError as exc:
            if 'syntax-highlighting' not in (exc.stderr or ''):
                raise
            result = subprocess.run(command + ['--no-highlight'], input=body, text=True,
                                    capture_output=True, check=True)
        return result.stdout


def render_house(source, body, style, labels, outputs):
    """One page in the house style's shape."""
    title, body = doc_layout.split_title(body)
    body = doc_layout.AUTHORED_TOPLINKS.sub('', body)
    reviews = source.with_name(source.stem + '_reviews.md')
    if reviews.exists():
        body = body.rstrip() + doc_layout.REVIEWS_DIVIDER + expand(reviews, source.parent) + '\n'
    header_text = HOUSE_HEADER.read_text(encoding='utf-8')
    out = run_pandoc_house(title or source.stem, body, header_text)
    cut = out.index('<body>')
    head, rest = out[:cut], out[cut:]
    rest = doc_layout.rewrite_body(rest)
    rest = re.sub(r'href="([^"#]+\.md)(#[^"]*)?"',
                  lambda m: link_target(source, m, outputs), rest)
    head = head.replace(STYLE_MARKER, style.block(), 1)
    nav = doc_layout.nav_bar(source.stem, labels)
    return doc_layout.assemble(head, rest, nav)


def link_target(source, match, outputs):
    absolute = (source.parent / match.group(1)).resolve()
    if absolute in outputs:
        return 'href="' + outputs[absolute] + (match.group(2) or '') + '"'
    return match.group(0)


def render_plain(source, body, nav):
    result = subprocess.run(['pandoc', '--from', 'gfm+fenced_divs', '--to', 'html5',
        '--standalone', '--metadata', 'title=' + source.stem,
        '--include-in-header', str(HEADER)], input=body, text=True,
        capture_output=True, check=True)
    return result.stdout.replace('<body>', '<body>\n' + nav, 1)


def build(folder, environ=None):
    """Render every numbered dossier page and return the output paths.

    environ is where the house style is looked up; it defaults to os.environ.
    """
    folder = Path(folder).resolve()
    docs = sorted(p for p in folder.glob('*.md')
                  if re.match(r'\d{2,}_', p.name) and not p.stem.endswith('_reviews'))
    if not docs:
        raise ValueError('No numbered dossier Markdown documents found')
    if not shutil.which('pandoc'):
        raise ValueError('HTML requires Pandoc; Markdown remains usable without it')
    style, note = doc_style.find_style(environ)
    if note:
        print(note, file=sys.stderr)
    outputs = {p.resolve(): p.with_suffix('.html').name for p in docs}
    stems = [p.stem for p in docs]
    labels = [(p.stem, label_for(p.stem, stems), outputs[p.resolve()]) for p in docs]
    plain_nav = '<nav aria-label="Dossier">' + ' '.join(
        '<a href="' + html.escape(href, quote=True) + '">' + html.escape(stem) + '</a>'
        for stem, _, href in labels) + '</nav>'
    rendered = []
    for source in docs:
        body = expand(source, folder)
        if style:
            page = render_house(source, body, style, labels, outputs)
        else:
            reviews = source.with_name(source.stem + '_reviews.md')
            if reviews.exists():
                body += '\n\n# Review history\n\n' + expand(reviews, folder)
            def rewrite(match, source=source):
                target, sep, fragment = match.group(1).partition('#')
                if '://' not in target and target and not target.startswith('#'):
                    absolute = (source.parent / target).resolve()
                    if absolute in outputs:
                        return '](' + outputs[absolute] + (sep + fragment if sep else '') + ')'
                return match.group(0)
            page = render_plain(source, re.sub(r'\]\(([^)]+)\)', rewrite, body), plain_nav)
        try:
            page = doc_diagrams.render(page, environ)
        except ValueError as exc:
            raise ValueError(source.name + ': ' + str(exc)) from exc
        rendered.append((source.with_suffix('.html'), page))
    # Validate and render every source before updating outputs.
    for target, page in rendered:
        target.write_text(page, encoding='utf-8')
        print(target)
    if style:
        doc_style.copy_fonts(style, folder)
    return [p for p, _ in rendered]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder')
    args = parser.parse_args()
    try:
        build(args.folder)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, str(exc) + '\n')

if __name__ == '__main__':
    main()
