# Expressive redesign — review notes

## Why the previous version felt static

The portrait appeared only after all projects. The hero used a small part of its available horizontal space, with typography and photography disconnected. All three projects shared the same preview-and-description pattern. The animation script only applied a small reveal to some below-fold project blocks; there was no hero choreography or mobile menu.

## Visual and interaction changes

The hero now places the real portrait beside the introduction, balanced with expressive sans and italic serif typography. A cobalt underlay and underline connect the portrait and headline without adding gradients or decorative illustrations. Supporting copy is concise.

MSN Academy uses a broad web/mobile composition and journey labels. Pickwise is a darker split composition with the research count alongside real prototype screens. Move Light reverses the split and layers two real application screens. The screen assets are not fabricated or edited.

The About section is shorter and uses a warm grey surface. A charcoal closing section carries the same serif language and accent family. This creates a light/dark rhythm without turning every project into the same card.

Initial hero text, portrait and actions overlap in a roughly 1.3-second entrance. Individual project compositions reveal on intersection, and screenshots respond on hover. Case-study links have a short 160ms response before navigation. The scroll cue repeats only four times and stops when scrolling begins. No loader, parallax, custom cursor or scroll trapping is used.

Mobile navigation uses a native modal dialog, staggered link entrances, Escape and close controls, explicit Tab containment, focus return and automatic closing on desktop resize. Without scripting, the regular navigation and all content remain visible. Reduced-motion preferences disable the motion and smooth scrolling, including when the preference changes mid-session.

The case-study research and substantive design explanations are preserved. Their typography, navigation, footer and media entrances now share the homepage language.

## Assets and performance

The approved JPEG matches the original `Black.jpg` in `Black.zip` byte-for-byte. The picture is not generated, retouched or cropped. Typography uses two self-hosted WOFF2 files totalling about 47 KB. Package archive integrity was verified. No animation library or frontend framework was added; the browser's Web Animations API handles motion, with CSS hover states.

The portrait is prioritised for loading. Project images are lazy-loaded. Videos remain user-controlled with no preloading. Transforms and opacity handle the main animated effects.

## Reference review limitations

The four supplied reference URLs were requested again before editing. Every request was blocked by the environment proxy with HTTP 403 / forbidden tunnel responses. Embedded sites could not be discovered or reviewed. This version follows the user's written creative direction and the audit of the existing implementation; it does not claim to reproduce or analyse inaccessible reference details.

## Preview and publication status

Work is isolated on `redesign/expressive-portfolio`. The main branch and production deployment are not updated. Browser walkthroughs and desktop/mobile screenshots are included for review. No authenticated Netlify CLI configuration, account binding, token or site ID was available, so no hosted preview is claimed. Use a separate manual Netlify test site or an authenticated draft deploy without `--prod` to review online.

## Remaining limitations

External demo, Figma, LinkedIn and reference destinations could not be independently checked through the restricted proxy. Their original URLs are preserved. The supplied resume PDF is unchanged. Pickwise remains an unlaunched concept with no second test round; its unresolved protection and failure paths are retained in the case study.

## Readability and interaction refinement

The follow-up review strengthened body weights, headline weights, supporting text colours and responsive type sizes. Small metadata is generally 11–12px; homepage descriptions are 15px on mobile and case-study body copy is 16px. Headings keep their deliberate line breaks on narrow screens. Supporting description contrast is approximately 8.7:1, and all branded Google/Coursera letters exceed 4.5:1 on their white surface. The Google palette uses darker brand-related shades for legibility, rather than low-contrast bright yellow.

Project surfaces now use 24–28px corners. Extra script annotations were removed to keep the screen compositions cleaner. Desktop pointer motion adds at most one degree of surface tilt, scheduled per animation frame; it is disabled for touch and reduced motion. A native 32px project cursor has a standard pointer fallback; no cursor-following element or hidden system cursor is used.

A three-pixel reading-position line and active section navigation help orientation. The copy-email button uses the Clipboard API with visible/live-region success or failure feedback and is hidden when the API or scripting is unavailable. The real email link remains available.
