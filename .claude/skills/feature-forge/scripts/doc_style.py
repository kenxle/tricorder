"""Find the house document style and read it, with no network access.

The style is the St. Clair document style that Lahe ships in its clone, under
vendor/stclair-doc-style/. A build looks for it in this order:

1. The FORGE_DOC_STYLE_DIR environment variable, a folder holding the style.
2. Lahe, found through the `lahe` command on PATH.

Lahe has no command that prints the location of its style, so step 2 reads the
command itself. The command is either a symlink to `<clone>/bin/lahe.js` or a
small shell wrapper that names that file by its absolute path.
"""
import os
import re
import shutil

STYLE_ENV = 'FORGE_DOC_STYLE_DIR'
# The attribute Lahe's own Markdown renderer puts on its inlined style. Lahe's
# style switcher looks for it, so a page that carries it can be restyled.
STYLE_ATTR = 'data-lahe-doc-style'
# Read in this order: the tokens, then the components that read them, then
# Lahe's layer over bare elements.
STYLE_FILES = ('system-tokens.css', 'document.css', 'lahe-markdown.css')
# A style missing any of these would leave the page half styled, so it is
# rejected instead of inlined.
MUST_HOLD = ('--surface', '.toplinks', '.contents-list', '.xref', '.status-dot')
FONT_URL = re.compile(r'\./\.lahe-fonts/([A-Za-z0-9._-]+\.woff2)')
SET_HINT = ('Set ' + STYLE_ENV + ' to a folder holding ' + ', '.join(STYLE_FILES) + '.')
NOT_FOUND = ('House style not found, so the pages use the plain offline style. '
             'Install Lahe so the lahe command is on PATH. ' + SET_HINT)


class Style:
    def __init__(self, css, folder, source):
        self.css = css
        self.folder = folder
        self.source = source

    def block(self):
        return '<style ' + STYLE_ATTR + '>\n' + self.css + '\n</style>'


def locate_lahe(environ):
    """Return (command, style folder) for the lahe command on PATH.

    command is None when there is no lahe command. The folder is None when the
    command is there but its clone cannot be worked out from it.
    """
    command = shutil.which('lahe', path=environ.get('PATH', ''))
    if not command:
        return None, None
    target = os.path.realpath(command)
    if not target.endswith(os.path.join('bin', 'lahe.js')):
        try:
            with open(target, encoding='utf-8', errors='replace') as handle:
                text = handle.read(8192)
        except OSError:
            return command, None
        found = (re.search(r'"(/[^"]*/bin/lahe\.js)"', text)
                 or re.search(r'(?<![\w.~/-])(/\S*/bin/lahe\.js)', text))
        if not found:
            return command, None
        target = found.group(1)
    clone = os.path.dirname(os.path.dirname(target))
    return command, os.path.join(clone, 'vendor', 'stclair-doc-style')


def _strip_token_import(css):
    """document.css opens by importing the tokens file. Once the files are one
    string the tokens already sit above it, and an import after other rules is
    invalid, so the line goes."""
    return re.sub(r'^\s*@import\s+url\(\s*["\']system-tokens\.css["\']\s*\)\s*;\s*$',
                  '', css, count=1, flags=re.M)


def read_style(folder, source):
    """Return (Style, None) for a usable folder, else (None, problem)."""
    files = {}
    for name in STYLE_FILES:
        path = os.path.join(folder, name)
        if not os.path.isfile(path):
            return None, name + ' is missing from ' + folder
        try:
            with open(path, encoding='utf-8') as handle:
                files[name] = handle.read()
        except (OSError, UnicodeDecodeError):
            return None, name + ' could not be read in ' + folder
        if not files[name].strip():
            return None, name + ' is empty in ' + folder
    css = '\n'.join(_strip_token_import(files[name]) for name in STYLE_FILES)
    missing = [marker for marker in MUST_HOLD if marker not in css]
    if missing:
        return None, 'the style in ' + folder + ' has no ' + ', '.join(missing)
    return Style(css, folder, source), None


def find_style(environ=None):
    """Return (Style or None, note or None).

    The note is one line for stderr. It comes with no style (the build falls
    back to the plain page) and also with a style when the variable was set but
    refused and Lahe's style was used instead. environ defaults to os.environ.
    """
    environ = os.environ if environ is None else environ
    refused = None
    override = environ.get(STYLE_ENV)
    if override:
        folder = os.path.abspath(os.path.expanduser(override))
        style, why = read_style(folder, STYLE_ENV)
        if style:
            return style, None
        refused = STYLE_ENV + ' is not usable: ' + why
    command, folder = locate_lahe(environ)
    problem = None
    if command and not folder:
        problem = ('found lahe at ' + command + ' but could not locate its style folder')
    elif folder:
        style, why = read_style(folder, 'Lahe')
        if style:
            note = refused + '; used the style from Lahe instead.' if refused else None
            return style, note
        problem = 'found lahe at ' + command + ' but its style is not usable: ' + why
    reasons = '; '.join(r for r in (refused, problem) if r)
    if reasons:
        return None, ('House style not found (' + reasons + '), so the pages use the '
                      'plain offline style. ' + SET_HINT)
    return None, NOT_FOUND


def copy_fonts(style, destination):
    """Copy the font files the style names beside the built pages.

    The style asks for ./.lahe-fonts/<name>.woff2. Lahe serves that path on a
    page it hosts, but a page opened from disk needs the files next to it.
    Returns the names copied.
    """
    names = sorted(set(FONT_URL.findall(style.css)))
    copied = []
    for name in names:
        source = os.path.join(style.folder, 'fonts', name)
        if not os.path.isfile(source):
            continue
        target_dir = os.path.join(destination, '.lahe-fonts')
        os.makedirs(target_dir, exist_ok=True)
        shutil.copyfile(source, os.path.join(target_dir, name))
        copied.append(name)
    return copied
