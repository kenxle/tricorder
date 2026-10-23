"""Render Pandoc Mermaid blocks locally as self-contained SVG images."""
import base64
import html
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET

CODE = re.compile(r'<pre\b([^>]*)>\s*<code\b([^>]*)>(.*?)</code>\s*</pre>', re.S)
CLASSES = re.compile(r'\bclass=["\']([^"\']*)["\']')
DIAGRAM_STYLE = ('<style>.forge-diagram{min-width:0;max-width:100%}'
                 '.forge-diagram-view{overflow-x:auto;max-width:100%}'
                 '.forge-diagram img{display:block;max-width:none;height:auto;'
                 'margin:0 auto}.forge-diagram figcaption{text-align:center}</style>')


def svg_image(svg):
    """Validate local assets and isolate SVG IDs/CSS in an image document."""
    try:
        root = ET.fromstring(svg)
    except ET.ParseError as exc:
        raise ValueError('Mermaid CLI produced invalid SVG: ' + str(exc)) from exc
    if root.tag != '{http://www.w3.org/2000/svg}svg':
        raise ValueError('Mermaid CLI did not produce an SVG diagram')
    for node in root.iter():
        tag = node.tag.rsplit('}', 1)[-1]
        if tag == 'script':
            raise ValueError('Mermaid diagram contains a script')
        for key, value in node.attrib.items():
            if key.rsplit('}', 1)[-1] in ('href', 'src') and tag != 'a':
                if not value.startswith(('#', 'data:')):
                    raise ValueError('Mermaid diagram requires a non-embedded resource')
    if re.search(r'@import\b|url\(\s*["\']?(?!#|data:)[^\s"\')]', svg, re.I):
        raise ValueError('Mermaid diagram contains external CSS resources')
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    title = root.find('svg:title', ns)
    desc = root.find('svg:desc', ns)
    title = ''.join(title.itertext()) if title is not None else 'Diagram'
    alt = ''.join(desc.itertext()) if desc is not None else title
    data = base64.b64encode(svg.encode('utf-8')).decode('ascii')
    dimensions = ''
    try:
        _, _, width, height = map(float, root.attrib['viewBox'].split())
        if all(math.isfinite(value) and value > 0 for value in (width, height)):
            width, height = math.ceil(width), math.ceil(height)
            dimensions = f' width="{width}" height="{height}" style="width:{width}px"'
    except (KeyError, ValueError):
        pass
    return ('<figure class="forge-diagram"><div class="forge-diagram-view" tabindex="0" '
            'role="region" aria-label="' + html.escape(title, quote=True) +
            '. Scroll horizontally if needed."><img src="data:image/svg+xml;base64,' + data +
            '" alt="' + html.escape(alt, quote=True) + '"' + dimensions + '></div><figcaption>' +
            html.escape(title) + '. Scroll horizontally if needed.</figcaption></figure>')


def render(page, environ=None):
    environ = os.environ if environ is None else environ
    def replace(match):
        classes = ' '.join(CLASSES.findall(match[1] + ' ' + match[2])).split()
        if not {'mermaid', 'language-mermaid'}.intersection(classes):
            return match[0]
        command = environ.get('FORGE_MERMAID_CLI') or shutil.which(
            'mmdc', path=environ.get('PATH', os.defpath))
        if not command:
            raise ValueError('Mermaid CLI is required for diagrams. Install '
                             '@mermaid-js/mermaid-cli and its browser, or set FORGE_MERMAID_CLI.')
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            source, output, config = folder / 'input.mmd', folder / 'output.svg', folder / 'config.json'
            source.write_text(html.unescape(match[3]), encoding='utf-8')
            config.write_text(json.dumps({'securityLevel': 'strict', 'htmlLabels': False,
                                          'theme': 'neutral', 'fontFamily': 'system-ui, sans-serif'}))
            try:
                result = subprocess.run([command, '-i', str(source), '-o', str(output),
                                         '-c', str(config), '-b', 'transparent'],
                                        capture_output=True, text=True, check=False,
                                        timeout=120)
            except (OSError, subprocess.TimeoutExpired) as exc:
                raise ValueError('Mermaid CLI could not render a diagram: ' + str(exc)) from exc
            if result.returncode or not output.is_file():
                raise ValueError('Mermaid diagram rendering failed: ' +
                                 (result.stderr.strip() or result.stdout.strip()))
            image = svg_image(output.read_text(encoding='utf-8'))
        return image + '\n<details><summary>Diagram source</summary>' + match[0] + '</details>'

    rendered = CODE.sub(replace, page)
    if rendered != page:
        rendered = rendered.replace('</head>', DIAGRAM_STYLE + '\n</head>', 1)
    return rendered
