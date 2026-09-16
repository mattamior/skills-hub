# Visual QA Guidance

Use this reference for final production assets, website integration, or a visual regression review.

## Master fidelity

- Compare every derivative against the approved master at a useful display size. Verify geometry, palette, stroke weight, wordmark case, lockup spacing, and background treatment.
- Do not pass an asset because its SVG paths look plausible. Rasterize and inspect the output.
- When a logo includes negative space or knockout shapes, inspect actual alpha values in standard transparent PNG exports. A hole intended to be transparent must have alpha `0`; a mask or coordinate-system mistake can look correct in source but fail after rendering.

## Accessibility and application color

Evaluate the accessibility requirements of the surface where brand colors are used. Do not apply interface contrast rules mechanically to approved logo artwork, but do not extend the logo exception to unrelated text, controls, states, or informational graphics.

When WCAG 2.2 Level AA applies, normal text needs at least 4.5:1 contrast and large-scale text at least 3:1. Visual information required to identify user-interface components or understand graphical objects generally needs at least 3:1 against adjacent colors. Text that is part of a logo or brand name is exempt from the text contrast minimum, but an interactive control surrounding a logo still needs an accessible presentation.

Record approved color pairings by role, including any colors that are decorative-only. Verify relevant default, hover, focus, selected, disabled, and error states when the brand implementation defines them. Do not use color as the sole means of communicating required meaning.

## Variant and localization checks

- Verify dark, light, black, and white variants use the approved outline and contrast treatment. Do not convert an approved colored outline to black or white unless that variant explicitly calls for it.
- Check 16px, 32px, and an application-size rendering. Simplify only if that simplification was explicitly approved; document it as a separate small-size variant.
- For maskable app icons, verify every essential part of the mark remains inside the guaranteed safe zone: a circle centered in the icon with radius 40% of the smaller image dimension. Test a safe-zone-only crop and representative circle/squircle masks. Use an opaque maskable background; do not confuse it with the transparent standard icon export.
- For required languages and scripts, verify glyph coverage, approved fallback fonts, shaping, line-height, casing behavior, and any localized wordmark or RTL-specific lockup. Do not infer approval of a localized composition from approval of the primary-language master.

## Delivery checks

- Parse SVG and verify it has no external dependencies, unexpected text/font dependency, malformed XML, or duplicate IDs.
- Verify PNG dimensions, color mode, and alpha behavior. Inspect ICO entries at each intended size.
- Request actual served favicon and manifest URLs from the running site or built static output. Browser tabs cache favicon candidates aggressively: use a versioned canonical URL when replacing an existing icon.
- For social metadata, verify the served image URL, actual dimensions, declared dimensions, and useful alternative text. If Open Graph emits `og:image`, verify `og:image:alt` is present. Re-check current target-platform requirements when the integration depends on them.
- Run the project's production build after web integration. Report browser, visual, accessibility, metadata, and build evidence separately; a successful build is not proof of visual fidelity or accessibility.
