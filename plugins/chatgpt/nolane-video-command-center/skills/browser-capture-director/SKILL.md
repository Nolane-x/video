---
name: browser-capture-director
description: Use when recording an authorized website, web app, product walkthrough, dashboard, browser interaction or HTML-native scene for a video.
---
# Browser Capture Director

## Capture truth
Use Playwright for deterministic browser state, screenshots and recorded interactions; use HyperFrames for HTML/CSS/GSAP scenes and composed browser-native video. Capture only sites/accounts the user is authorized to access.

## Workflow
1. Define the exact page, routes, user journey, viewport, device scale, color scheme, locale, FPS and cursor behavior.
2. Use a dedicated test account and synthetic data where possible. Mask or avoid personal records, tokens, inboxes, customer identifiers and other sensitive content.
3. Confirm the target app is in the expected build/version/state. Record the source commit/deployment URL and timestamp.
4. Disable nondeterministic animation or wait for stable states where possible; set explicit viewport, clock/seed and network fixtures for repeatable capture.
5. Capture only the relevant path. Do not click destructive actions, submit forms, purchase, publish or mutate user data unless the user explicitly authorized that action.
6. Inspect screenshots and continuous playback for broken text, loading skeletons, tooltips, browser chrome, hover artifacts, cursor occlusion, scroll jumps, layout shifts and accidental personal data.
7. Keep original captures separate from edited/composited overlays; exact text and callouts should remain editable.
8. Log any unavailable page, blocked network request, auth failure or substituted synthetic view. Never present a synthetic recreation as a real capture.

## Privacy and rights
Respect site terms, robots/access boundaries and the user's authorization. Do not bypass paywalls or access controls. Redact secrets and private data before artifact upload. Website branding/content may require separate permission for public or commercial use.

## Handoff
Provide route/step list, viewport, browser/runtime version, source URL/build, capture files, masked-data note, reproducibility steps and visual QA.
