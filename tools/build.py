#!/usr/bin/env python3
"""Build the manual: src/<lang>/*.html fragments -> docs/ (English, the default) and docs/zh/ (Chinese).

    python3 tools/build.py

A page is an HTML fragment whose first line is a comment with its title and one-line
summary:  <!-- title | summary -->
NAV below is the one list of pages. A page that exists in one language and not the
other is listed as "being written" in the language that lacks it, and the language
switch on such a page goes to the other language's home.
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, OUT = os.path.join(ROOT, "src"), os.path.join(ROOT, "docs")

# (page, Chinese label, English label)
NAV = [
    (("开始", "Start"), [("index", "首页", "Home"), ("start", "需要准备什么", "What you need")]),
    (("安装 rtl_tcp", "Install rtl_tcp"), [("install-macos", "macOS", "macOS"), ("install-windows", "Windows", "Windows"),
                                         ("install-linux", "Linux", "Linux"), ("install-pi", "树莓派", "Raspberry Pi"),
                                         ("bridge-bl618", "BL618 无线小板", "BL618 Wi-Fi board")]),
    (("连接", "Connect"), [("connect", "在 App 里连接", "Connect in the app"),
                         ("troubleshoot", "连不上怎么办", "If it will not connect")]),
    (("航图数据", "Airspace data"), [("aip-import", "直接导入各国 AIP", "Importing an AIP directly"),
                                    ("data-file", "航图数据文件（JSON）", "Airspace data file (JSON)")]),
    (("各页面说明", "The pages"), [("pages", "页面一览", "All pages"), ("page-radio", "Radio 收音机", "Radio"),
                              ("page-receiver", "Receiver 接收机", "Receiver"),
                              ("page-dstar", "D-STAR 数字语音", "D-STAR digital voice"),
                              ("page-aviation", "Aviation 航空数据链", "Aviation"),
                              ("page-atc", "ATC 航空管制", "ATC"), ("page-aprs", "APRS", "APRS"),
                              ("page-ais", "AIS 船舶", "AIS"), ("page-adsb", "ADS-B 飞机", "ADS-B")]),
]

TEXT = {
    "zh": dict(lang="zh-Hans", site="使用手册", suffix="SDRViewer 使用手册", soon="编写中", prev="上一篇", next="下一篇",
               other="English", menu="目录", theme="切换深色或浅色", copy="复制", copied="已复制",
               footer="SDRViewer 使用手册 · 内容随 App 更新。发现错误或有看不懂的地方，欢迎告诉作者。"),
    "en": dict(lang="en", site="Manual", suffix="SDRViewer Manual", soon="soon", prev="Previous", next="Next",
               other="中文", menu="Contents", theme="Light or dark", copy="Copy", copied="Copied",
               footer="SDRViewer Manual · updated with the app. If something is wrong or unclear, tell the author."),
}

LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#0a7cff"/>'
        '<path d="M5 20c2.5 0 2.5-9 5-9s2.5 12 5 12 2.5-15 5-15 2.5 12 5 12 1.7-4 2-4" fill="none" '
        'stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>')

TEMPLATE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · {suffix}</title>
<meta name="description" content="{summary}">
<link rel="stylesheet" href="{base}assets/style.css">
<script>window.MANUAL = {{copy: "{copy}", copied: "{copied}"}};</script>
<script src="{base}assets/site.js"></script>
</head>
<body data-soon="{soon}">
<header class="top">
  <button class="iconbtn" id="menu" aria-label="{menu}">☰</button>
  <a class="brand" href="index.html">{logo}<span>SDRViewer <small>{site}</small></span></a>
  <span class="spacer"></span>
  <a class="iconbtn langlink" href="{other_href}">{other}</a>
  <button class="iconbtn" id="theme" aria-label="{theme}">◐</button>
</header>
<div class="layout">
<nav class="side">
{nav}
</nav>
<main>
{body}
{pager}
<footer>{footer}</footer>
</main>
</div>
</body>
</html>
"""


def read(lang, name):
    path = os.path.join(SRC, lang, name + ".html")
    if not os.path.exists(path):
        return None
    text = open(path, encoding="utf-8").read()
    m = re.match(r"\s*<!--\s*(.*?)\s*\|\s*(.*?)\s*-->\s*", text, re.S)
    if not m:
        sys.exit(f"{lang}/{name}.html: the first line must be <!-- title | summary -->")
    return m.group(1), m.group(2), text[m.end():]


# The language served at the site's root; the other lives in its own folder.
ROOT = "en"


def build(lang):
    t = TEXT[lang]
    other = "en" if lang == "zh" else "zh"
    column = 1 if lang == "zh" else 2
    names = [item[0] for _, items in NAV for item in items]
    pages = {name: read(lang, name) for name in names}
    others = {name: read(other, name) is not None for name in names}
    order = [name for name in names if pages[name]]
    out_dir = OUT if lang == ROOT else os.path.join(OUT, lang)
    os.makedirs(out_dir, exist_ok=True)
    base = "" if lang == ROOT else "../"
    for name in order:
        title, summary, body = pages[name]
        nav = []
        for heading, items in NAV:
            nav.append(f"<h4>{html.escape(heading[column - 1])}</h4>")
            for item in items:
                label = html.escape(item[column])
                if pages[item[0]] is None:
                    nav.append(f'<a class="soon">{label}</a>')
                else:
                    on = ' class="on"' if item[0] == name else ""
                    nav.append(f'<a{on} href="{item[0]}.html">{label}</a>')
        i = order.index(name)
        pager = ['<div class="pager">']
        if i > 0:
            pager.append(f'<a href="{order[i-1]}.html"><small>{t["prev"]}</small>{html.escape(pages[order[i-1]][0])}</a>')
        if i + 1 < len(order):
            pager.append(f'<a class="next" href="{order[i+1]}.html"><small>{t["next"]}</small>{html.escape(pages[order[i+1]][0])}</a>')
        pager.append("</div>")
        target = name if others[name] else "index"
        other_href = (f"{other}/{target}.html" if lang == ROOT else f"../{target}.html")
        # Fragments name images and assets as on the root-language page.
        body = body.replace('src="img/', f'src="{base}img/')
        body = body.replace('href="data/', f'href="{base}data/')
        page = TEMPLATE.format(title=html.escape(title), summary=html.escape(summary), logo=LOGO, base=base,
                               nav="\n".join(nav), body=body, pager="\n".join(pager), other_href=other_href,
                               **{k: t[k] for k in ("lang", "site", "suffix", "soon", "other", "menu", "theme",
                                                    "copy", "copied", "footer")})
        with open(os.path.join(out_dir, name + ".html"), "w", encoding="utf-8") as f:
            f.write(page)
    return len(order), sum(1 for p in pages.values() if p is None)


def main():
    for lang in ("zh", "en"):
        done, missing = build(lang)
        print(f"{lang}: built {done} pages; {missing} still to write")


if __name__ == "__main__":
    main()
