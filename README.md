# Mariyam Muneer — expressive portfolio review

This is a substantial visual and interaction redesign of the existing static portfolio. It uses the original HTML pages, project media, resume, contact links and Netlify structure. No framework migration, build command or package installation is needed to run it.

## Preview and approval

Review branch: `redesign/expressive-portfolio`. This branch is separate from `main`. No production deployment has been performed.

- `review/desktop-walkthrough.mp4`: recorded browser walkthrough showing the hero entrance, scrolling compositions and hover behaviour.
- `review/hero-desktop.png` and `review/hero-mobile.png`: opening-screen previews.
- `portfolio-final.zip`: ready-to-extract review build, with `index.html` at the archive root. Large review recordings/screenshots are excluded from this deployment ZIP.

For a working local preview, extract the ZIP, open a terminal in that folder and run:

```sh
python -m http.server 8090
```

Then open the local address shown by Python. Everything runs without a JavaScript framework or external runtime assets.

An authenticated Netlify preview could not be created: the environment has no Netlify account binding, token or site association. To review online, use a separate manual Netlify test site, or an authenticated draft deploy of the extracted folder to the existing site **without `--prod`**. Neither GitHub `main` nor the existing Netlify production site should be replaced until this version is approved.

After approval, use the existing manual Netlify deployment workflow with the extracted folder. Preserve `netlify.toml`: publish directory `.`, build command blank.

## What changed

- A portrait-led asymmetrical hero with staged text, image and action entrances.
- Warm ivory, charcoal and a restrained cobalt accent.
- Locally hosted Manrope and Instrument Serif typography.
- Three distinct project compositions, ordered MSN Academy, Pickwise, Move Light, with clean 24–28px rounded surfaces.
- Larger, more firmly weighted typography and darker supporting text across desktop and mobile.
- Contrast-safe Google lettering and Coursera styling linked to the foundations course.
- Short homepage writing; research evidence and limitations remain inside the case studies.
- Native-dialog mobile navigation, keyboard focus handling, image expansion and quick case-study transitions.
- Scroll reveals and hover responses implemented with the Web Animations API and CSS. Reduced-motion and no-JavaScript paths are supported.
- Subtle desktop pointer tilt, a contextual native project cursor, reading progress, active navigation and accessible copy-email feedback.

## Content and portrait

The approved JPEG from `Black.zip` remains unchanged at `assets/mariyam-professional-portrait.jpg`. The hero displays the original image without generation, retouching, recolouring or a crop; the surrounding frame is styled in CSS.

Your Biotechnology studies, Google UI/UX foundations through Coursera and vibe coding with Codex and Claude remain in About. No course completion or certificate is claimed. The original resume PDF is preserved.

MSN Academy distinguishes shared audit work, your desktop/design/handoff responsibilities, your teammate's mobile prototype and the developer-built demo. Pickwise retains the corrected participant mix, four-week duration and untested redesign limitations. Move Light separates design direction from AI-generated implementation. The old Velora and Nourish Lab URLs remain available but unfeatured.

## Validation

Start the local server on port 8090, then run:

```sh
python review/check_expressive.py
python review/check_readability.py
node --check site.js
```

The browser test requires Python Playwright and Chromium at `/usr/bin/chromium`; these are testing tools, not app runtime dependencies. Override `PORTFOLIO_TEST_URL` or `PORTFOLIO_TEST_OUTPUT` if needed.

See `review/expressive-test-results.txt`, `review/readability-test-results.txt`, `review/animation-evidence.json` and `review/expressive-design-notes.md`. There is no package-based build or lint script in this static project.

## Fonts

The two WOFF2 files are self-hosted, with the original font licenses in `assets/fonts/`. They came from Fontsource packages at version 5.3.0; archive SHA-512 integrity was checked against registry metadata. No font service request is made at runtime.
