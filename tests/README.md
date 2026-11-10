# Orbit tests

- `python3 tests/contrast.py` checks tier/group colors and text colors against WCAG AA, in light and dark.
- `python3 -m http.server 8765` from the repo root, then `python3 tests/run.py [screenshot dir]` runs the browser tests (Playwright, Chromium): Today cap, person page order, groups and timing, bulk add with duplicates, merge restore, Undo timing, Recent view, dark mode, tour, first run, 59-person stress set, desktop.
- `seed.py` holds the 9 sample people.
