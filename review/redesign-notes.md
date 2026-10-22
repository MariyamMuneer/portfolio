> Historical notes for the previous editorial version. See `expressive-design-notes.md` for the current review build.

# Redesign review

## Source availability and audit

The existing static source and original upload ZIP were present. The project media, Pickwise notes and research synthesis were also retained. Existing framework: plain HTML with a shared stylesheet; Netlify publish directory `.`. No rebuild or dependency installation was necessary.

Issues identified before editing:

- MSN Academy was not the lead project despite its real team/handoff context.
- Five projects competed for attention; Velora weakened the requested hierarchy.
- Repeated process prose, inconsistent headings and uneven case-study length slowed scanning.
- A generated portrait was being used instead of the newly approved photo.
- A repeated dark/green card system and dense project navigation limited the editorial direction.
- Shared contributions and AI-assisted implementation needed clearer labels.

## Reference access

Read-only requests were attempted for the current site and all four supplied reference URLs. The environment's network proxy returned HTTP 403 / forbidden tunnel responses for all five. Embedded portfolio URLs could not be inspected. No claim is made that the reference typography, composition, animations or responsiveness were reviewed. The design follows the written brief and source audit; no reference layout or code was copied.

## Visual direction and information architecture

An off-white, charcoal and grey editorial identity. Project screens provide the colour. System sans-serif type is paired with restrained Georgia italics, avoiding remote fonts and runtime dependencies. Generous spacing and large project previews lead the hierarchy.

Home: introduction → MSN Academy → Pickwise → Move Light → About → Contact.
Navigation: Work / About / Resume / Contact.
Case studies: concise overview and scope → evidence and responsibilities → decisions → selected screens → feedback, limitations and learning.

Velora and Nourish Lab remain reachable at their existing URLs but are not in the featured work or the next-project sequence. No unfinished future project is displayed.

## Implemented interactions

- Subtle below-fold project reveals using IntersectionObserver; content is visible by default.
- Small image-scale and link transitions; no parallax or custom cursor.
- Image expansion in a native dialog, with Escape, close button and focus restoration.
- Direct image links still work without JavaScript.
- Native expandable research decision log.
- Reduced-motion mode disables animated scrolling and reveal hiding.

## Content accuracy

MSN Academy distinguishes the designer's roadmap, wireframes, UI, desktop prototype and handoff from shared audit work, the teammate's mobile prototyping and developer implementation. There was no student usability study.

Pickwise retains participant counts, convenience-sample limitations, before/after evidence and unresolved protection, returns, verification and seller-flow issues. No adoption or conversion result is claimed.

Move Light distinguishes design direction from generated code and avoids unsupported long-term results.

The About section briefly includes Biotechnology studies, design foundations through Google's UI/UX course on Coursera, and vibe coding with Codex and Claude. No certificate completion is claimed.

## Missing assets and access

- The approved portrait was subsequently supplied in `Black.zip`. Its original JPEG is now included unchanged, with its original aspect ratio. The placeholder is removed.
- Nourish Lab screenshot assets were missing from the original upload. The retained exploration is text-based and links to its original Figma file.
- Netlify authentication/site configuration was unavailable. No online preview or production deployment was created.
- External project demo, LinkedIn and Figma links were preserved; destination availability could not be verified through the restricted proxy.
- The source resume PDF is preserved and has not been edited to include the new course information.

## Review before publishing

Review the supplied portrait, screen compositions and current resume. A manually deployed production site remains unchanged until the user uploads the reviewed package. `netlify.toml` is preserved byte-for-byte. The user subsequently requested replacement of the older GitHub portfolio. The redesigned files and updated root ZIP are published to `main`; no Netlify production publish was attempted.
