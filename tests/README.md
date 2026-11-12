# Orbit tests

- `python3 tests/contrast.py` checks tier/group colors and text colors against WCAG AA, in light and dark.
- `python3 -m http.server 8765` from the repo root, then `python3 tests/run.py [screenshot dir]` runs the browser tests (Playwright, Chromium): Today cap, person page order, groups and timing, bulk add with duplicates, merge restore, Undo timing, Recent view, dark mode, tour, first run, 59-person stress set, desktop.
- `seed.py` holds the 9 sample people.
- Arabic: the interface strings live in `ar.js` (built from `tests/i18n/dict/*.py` by `tests/i18n/build.py` then `tests/i18n/mkjs.py`; run them from a folder holding the crawl output). `tests/i18n_crawl.py` lists every string the app shows; `tests/ar_check.py` lists anything still English with the app in Arabic.
