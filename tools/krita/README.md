# Krita asset workflow

Krita is an art-authoring tool, not a runtime dependency for every render. Use it to create assets with human art direction rather than asking code to invent every visual detail.

## Assets worth hand-authoring

- Character silhouette and expression sheet
- Hand gestures and action poses
- Phone, notebook, calendar, staircase, door, and other story props
- Paper grain, pencil marks, and subtle background texture
- Paint-over fixes for awkward poses or tangencies

## Export rules

1. Keep the editable `.kra` source with the project's original assets.
2. Export transparent PNG for cut-out props or character parts.
3. Export background plates separately from foreground characters when parallax is needed.
4. Use consistent canvas size, anchor points, and naming (for example `mascot_idle.png`, `mascot_phone.png`, `prop_phone.png`).
5. Record attribution and license for any imported image, brush, texture, or font.

## Style direction

Use the H2 minimalist world: cream mascot, charcoal/graphite backgrounds, slate clothing, limited muted red as the temptation accent, and occasional warm light to signal resolution. Avoid glossy AI gradients, pseudo-photoreal skin, and unnecessary detail.

Krita does not need to be installed on GitHub Actions simply to render the Remotion project. Only add a Krita batch-export step if a future project requires an actual `.kra` file transformation.
