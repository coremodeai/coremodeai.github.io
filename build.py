#!/usr/bin/env python3
"""Build coremode.ai.

    python3 build.py

Reads src/pages/*.html, wraps each in the shared header and footer, and writes
the finished page to the repository root, where GitHub Pages serves it.
No dependencies. The build fails if a page breaks the design rules in DESIGN.md.
"""
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"

# ---- navigation: the one place the menus are defined ------------------------
# (label, href) or (label, href, tag)
NAV = [
    {"label": "Platform", "href": "platform.html", "groups": [
        ("Align", [("Objectives", "platform.html#objectives"), ("Knowledge", "platform.html#knowledge")]),
        ("See", [("Focus", "platform.html#focus"), ("Signals", "platform.html#signals"),
                 ("Perspective", "platform.html#perspective")]),
        ("Act", [("Actions", "integrations.html#actions"), ("Integrations", "integrations.html")]),
    ]},
    {"label": "Solutions", "href": "solutions.html", "groups": [
        ("Roles", [("Leaders", "solutions.html#leaders"), ("Managers", "solutions.html#managers"),
                   ("Everyone", "solutions.html#everyone")]),
        ("Needs", [("Alignment", "solutions.html#alignment"), ("Decisions", "solutions.html#decisions"),
                   ("Follow-through", "solutions.html#follow-through")]),
    ]},
    {"label": "Resources", "href": "resources.html", "groups": [
        ("Help", [("Request a demo", "resources.html#demo"), ("Support", "resources.html#support")]),
        ("Learn", [("How it works", "resources.html#how"), ("Guides", "resources.html#guides", "Soon"),
                   ("Developers", "resources.html#developers", "Soon")]),
        ("Trust", [("Privacy", "privacy.html")]),
    ]},
    {"label": "Enterprise", "href": "enterprise.html"},
    {"label": "Pricing", "href": "pricing.html"},
]
# Old addresses that now live elsewhere.
REDIRECTS = {"how.html": "resources.html#how"}
SIGN_IN = "https://login.coremode.ai/"
SIGN_UP = "signup.html"

# ---- icons: 24px, one stroke weight -----------------------------------------
ICONS = {
    "target": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/><path d="m14.5 9.5 5-5M16.5 4.5h3v3"/>',
    "layers": '<path d="M12 3.5 20.5 8 12 12.5 3.5 8z"/><path d="m3.5 12 8.5 4.5 8.5-4.5M3.5 16l8.5 4.5 8.5-4.5"/>',
    "pulse": '<path d="M3 12h3.5l2.5-6.5 4.5 13 2.5-6.5H21"/>',
    "people": '<circle cx="9" cy="8" r="3.5"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M17 8h4M19 6v4"/>',
    "server": '<rect x="4" y="4" width="16" height="6" rx="1.5"/><rect x="4" y="14" width="16" height="6" rx="1.5"/><path d="M8 7h.01M8 17h.01"/>',
    "record": '<path d="M7 3h7l4 4v14H7zM14 3v4h4M10 12h5M10 16h5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
}


def icon(name):
    return ('<svg class="cell__icon" width="24" height="24" viewBox="0 0 24 24" fill="none" '
            'stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{ICONS[name]}</svg>')


CHEVRON = ('<svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" '
           'stroke-width="1.5" aria-hidden="true"><path d="m2 3.5 3 3 3-3"/></svg>')


def menu_link(item, cls):
    label, href = item[0], item[1]
    tag = f' <span class="tag">{item[2]}</span>' if len(item) > 2 else ""
    return f'<a class="{cls}" href="{href}">{label}{tag}</a>'


def groups_html(groups, link_cls):
    out = []
    for name, items in groups:
        links = "".join(menu_link(i, link_cls) for i in items)
        out.append(f'<div><p class="menu__label">{name}</p>{links}</div>')
    return "".join(out)


def header(page):
    links = []
    for top in NAV:
        current = ""
        if top["href"] == page:
            current = ' aria-current="page"'
        elif any(i[1].split("#")[0] == page for _, items in top.get("groups", []) for i in items):
            current = ' aria-current="true"'
        if "groups" in top:
            links.append(
                f'<div class="nav__item"><a class="nav__link" href="{top["href"]}"{current}>'
                f'{top["label"]} {CHEVRON}</a>'
                f'<div class="menu"><div class="menu__inner wrap">{groups_html(top["groups"], "menu__link")}</div></div></div>')
        else:
            links.append(f'<a class="nav__link" href="{top["href"]}"{current}>{top["label"]}</a>')

    sheet = []
    for top in NAV:
        if "groups" in top:
            sheet.append(groups_html(top["groups"], "footer__link"))
    plain = "".join(f'<a class="footer__link" href="{t["href"]}">{t["label"]}</a>' for t in NAV if "groups" not in t)
    sheet.append(f'<div><p class="menu__label">More</p>{plain}'
                 f'<a class="footer__link" href="{SIGN_IN}">Sign in</a>'
                 f'<a class="footer__link" href="{SIGN_UP}">Sign up</a></div>')

    return f'''<header class="nav">
      <div class="nav__bar wrap">
        <a class="brand" href="index.html" aria-label="coremode home">
          <img src="assets/mark.svg" alt="" width="24" height="24" />coremode
        </a>
        <nav class="nav__links" aria-label="Site">{"".join(links)}</nav>
        <div class="nav__auth">
          <a class="nav__link" href="{SIGN_IN}">Sign in</a>
          <a class="button button--small" href="{SIGN_UP}">Sign up</a>
        </div>
        <details class="nav__mobile">
          <summary class="button button--quiet button--small">Menu</summary>
          <nav class="nav__sheet" aria-label="Site, compact">{"".join(sheet)}</nav>
        </details>
      </div>
    </header>'''


def footer():
    cols = []
    for top in NAV:
        if "groups" in top:
            items = [i for _, group in top["groups"] for i in group]
            links = "".join(menu_link(i, "footer__link") for i in items)
            cols.append(f'<div><p class="menu__label">{top["label"]}</p>{links}</div>')
    plain = "".join(f'<a class="footer__link" href="{t["href"]}">{t["label"]}</a>' for t in NAV if "groups" not in t)
    cols.append(f'<div><p class="menu__label">Company</p>{plain}'
                f'<a class="footer__link" href="{SIGN_UP}">Sign up</a>'
                f'<a class="footer__link" href="{SIGN_IN}">Sign in</a></div>')
    return f'''<footer class="footer">
      <div class="wrap">
        <div class="footer__grid">
          <div>
            <a class="brand" href="index.html" aria-label="coremode home">
              <img src="assets/mark.svg" alt="" width="24" height="24" />coremode
            </a>
          </div>
          {"".join(cols)}
        </div>
        <p class="note">No cookies. Nothing loaded from anyone else.</p>
      </div>
    </footer>'''


LAYOUT = '''<!doctype html>
<!-- Built by build.py from src/pages/{name}. Edit the source, not this file. -->
<html lang="en" data-theme="dark">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <meta name="description" content="{description}" />
    <link rel="icon" href="assets/mark.svg" type="image/svg+xml" />
    <link rel="stylesheet" href="assets/tokens.css" />
    <link rel="stylesheet" href="assets/styles.css" />
  </head>
  <body>
    {header}

    <main class="wrap">
{content}
    </main>

    {footer}
  </body>
</html>
'''

# ---- design rules, checked on every build -----------------------------------
MAX_WORDS = 28      # in any one paragraph, list item or definition
MAX_H1 = 60         # characters
MAX_TITLE = 65
MAX_DESCRIPTION = 160


def text_of(fragment):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", fragment))).strip()


def lint_css(errors):
    css = re.sub(r"/\*.*?\*/", "", (ROOT / "assets/styles.css").read_text(), flags=re.S)
    for raw in sorted(set(re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(", css))):
        errors.append(f"styles.css: raw colour {raw!r}; use a --color token")
    for prop, ok in (("font-size", r"var\(--text-"), ("font-weight", r"var\(--weight-"),
                     ("border-radius", r"var\(--radius-")):
        for value in re.findall(rf"(?<![-\w]){prop}:\s*([^;}}]+)", css):
            if not re.match(ok, value.strip()):
                errors.append(f"styles.css: {prop}: {value.strip()}; use a token")
    return set(re.findall(r"\.([a-zA-Z][\w-]*)", css))


def lint_page(name, meta, body, built, defined, used, errors):
    if len(meta["title"]) > MAX_TITLE:
        errors.append(f"{name}: title is {len(meta['title'])} characters; the limit is {MAX_TITLE}")
    if len(meta["description"]) > MAX_DESCRIPTION:
        errors.append(f"{name}: description is {len(meta['description'])} characters; the limit is {MAX_DESCRIPTION}")
    if re.search(r"\sstyle=", body):
        errors.append(f"{name}: inline style; use a component")
    if len(re.findall(r"<h1[\s>]", body)) != 1:
        errors.append(f"{name}: needs exactly one h1")
    for h1 in re.findall(r"<h1[^>]*>(.*?)</h1>", body, flags=re.S):
        if len(text_of(h1)) > MAX_H1:
            errors.append(f"{name}: h1 is {len(text_of(h1))} characters; the limit is {MAX_H1}")
    for block in re.findall(r"<(?:p|li|dd)[^>]*>(.*?)</(?:p|li|dd)>", body, flags=re.S):
        words = len(text_of(block).split())
        if words > MAX_WORDS:
            errors.append(f"{name}: {words} words in one block; the limit is {MAX_WORDS}: “{text_of(block)[:60]}…”")
    for attr in re.findall(r'class="([^"]*)"', built):
        for cls in attr.split():
            used.add(cls)
            if cls not in defined:
                errors.append(f"{name}: class “{cls}” is not a component in styles.css")


def build():
    errors, used = [], set()
    defined = lint_css(errors)
    partials = {p.stem: p.read_text().rstrip() for p in (SRC / "partials").glob("*.html")}
    pages = sorted((SRC / "pages").glob("*.html"))
    for path in pages:
        source = path.read_text()
        head = re.match(r"<!--(.*?)-->\s*", source, flags=re.S)
        if not head:
            sys.exit(f"{path.name}: starts with no <!-- title / description --> block")
        meta = dict(re.findall(r"^\s*(\w+):\s*(.+?)\s*$", head.group(1), flags=re.M))
        body = source[head.end():].rstrip()
        body = re.sub(r"\{\{icon:(\w+)\}\}", lambda m: icon(m.group(1)), body)
        body = re.sub(r"\{\{(\w+)\}\}", lambda m: partials[m.group(1)], body)
        built = LAYOUT.format(name=path.name, title=html.escape(meta["title"]),
                              description=html.escape(meta["description"], quote=True),
                              header=header(path.name), content=body, footer=footer())
        lint_page(path.name, meta, body, built, defined, used, errors)
        (ROOT / path.name).write_text(built)
    for old, new in REDIRECTS.items():
        (ROOT / old).write_text(
            '<!doctype html>\n<html lang="en">\n  <head>\n    <meta charset="utf-8" />\n'
            f'    <title>coremode</title>\n    <meta http-equiv="refresh" content="0; url={new}" />\n'
            f'    <link rel="canonical" href="{new}" />\n  </head>\n'
            f'  <body><a href="{new}">This page has moved.</a></body>\n</html>\n')
    for cls in sorted(defined - used):
        errors.append(f"styles.css: “.{cls}” is used by no page; remove it")
    if errors:
        print("\n".join(errors))
        sys.exit(f"\n{len(errors)} problem(s). Pages were written, but fix these before pushing.")
    print(f"Built {len(pages)} pages. Design rules pass.")


if __name__ == "__main__":
    build()
