# SDRViewer Manual · SDRViewer 使用手册

The user manual for SDRViewer, an RTL-SDR receiver app for iPhone and iPad, in Chinese and English.

SDRViewer（iPhone / iPad 上的 RTL-SDR 接收机）的使用手册，中英文两种语言。

**Read it online · 在线阅读：** https://nasacj.github.io/SDRViewer-Manual/

## Editing · 修改

Pages are HTML fragments in `src/zh` and `src/en`; the first line of each is a comment
holding its title and summary. `tools/build.py` wraps them in the shared layout and
writes the site to `docs/`, which GitHub Pages serves.

```sh
python3 tools/build.py      # needs only Python 3
open docs/index.html        # preview
```

The list of pages and their order is `NAV` in `tools/build.py`. A page that exists in
only one language shows as "being written" in the other.

Screenshots go in `docs/img`. They are taken with demonstration data and example
addresses, and carry nothing personal.
