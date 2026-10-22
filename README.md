# Mariyam Muneer — portfolio

A lightweight static portfolio, retaining the existing HTML/CSS asset structure and Netlify configuration. No framework, package install or build step is required.

## Preview locally

From the portfolio directory:

```sh
python -m http.server 8080
```

Open the local address shown by Python. The homepage is `index.html`. The featured case studies are `msn-academy.html`, `pickwise.html` and `move-light.html`.

## Approved portrait

The exact approved photo from `Black.zip` is included at `assets/mariyam-professional-portrait.jpg`. The JPEG bytes are unchanged from the uploaded `Black.jpg`; no generation, retouching, recolouring or cropping was performed. The image uses its original dimensions and proportions. The old generated photo and temporary placeholder are removed.

## Netlify deployment after approval

The existing `netlify.toml` is unchanged: publish directory `.`; no build command.

1. Extract `portfolio-final.zip` to a new empty folder. `index.html`, `style.css`, `site.js`, `netlify.toml` and `assets/` should be at its root.
2. Preview the folder locally and review the portrait before publication.
3. To review online without altering production, create a separate manual Netlify site or use an authenticated draft deploy (`netlify deploy --dir <folder> --site <existing-site-id>` without `--prod`). Netlify access is required; no credentials were available during this redesign.
4. After approval, upload the extracted folder through the existing site's manual deploy workflow, or run a production deploy using your authenticated Netlify setup.

No GitHub connection is needed. The redesign was developed on `redesign/editorial-portfolio` and replaces the earlier files on the GitHub `main` branch at the user’s request. No Netlify deployment was performed.

## Content and links

The original project media and functional links are retained. Velora and Nourish Lab keep their URLs for existing visitors, but are not featured. No unfinished SaaS project is displayed. The resume PDF is the existing supplied file; it has not been rewritten.

Pickwise follows the final case-study notes: four weeks; five participants, three with OLX experience and two without second-hand experience; the redesign was not re-tested. The About section mentions the Google UI/UX course on Coursera without claiming completion or certification, plus Biotechnology studies and vibe coding with Codex and Claude.

See `review/redesign-notes.md` and `review/test-results.txt` for scope, limitations and validation.

## Validation

Browser checks are recorded in `review/test-results.txt`. To rerun, start the local server on port 8080, then run `python review/check_portfolio.py` in an environment with Python Playwright and `/usr/bin/chromium`. Generated review screenshots are ignored by Git. Run `node --check site.js` for JavaScript syntax. No package-based build or lint scripts existed in the original static project.
