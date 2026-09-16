# Production Asset Guidance

Use this reference only after a logo direction has been approved, or when auditing a final brand pack.

## Choose the asset set by use case

Start with a vector master and publish only variants that serve an identified surface:

- **Logo system:** mark, wordmark, and lockups only when each will be used. Include light, dark, monochrome, and reverse variants only where contrast or production constraints require them.
- **Web app:** SVG brand mark/lockup as needed; favicon PNG sizes and ICO; Apple touch icon; PWA icons and manifest only if the application uses a manifest.
- **Maskable icons:** use an opaque safe-zone background only for the maskable export. Keep all important content inside the Web App Manifest safe zone: a centered circle with radius 40% of the smaller icon dimension. The visual mark's intended negative space must still read correctly against that background.
- **Social sharing:** create Open Graph or platform-specific images only when metadata will reference them. Verify current platform guidance when possible; treat any fallback dimensions as documented assumptions, not timeless brand invariants. When Open Graph metadata uses `og:image`, also provide the applicable structured metadata such as dimensions and `og:image:alt`.
- **Print or external handoff:** preserve an editable vector master and document the exact colors, clear space, minimum size, and production constraints before creating raster derivatives.

## Vector and raster rules

- Keep production SVGs self-contained: no external images, stylesheets, or font dependencies. Convert final wordmarks to paths when cross-device consistency is required and font licensing allows it.
- Preserve the approved viewBox, proportions, stroke widths, joins, and colors. Derivatives may scale or crop only where their format calls for it.
- Raster exports must be generated from the approved master, not redrawn separately. Retain transparency wherever the asset is expected to overlay arbitrary backgrounds.
- Name files by role and background treatment, for example `mark-color-on-dark.svg`, `lockup-horizontal-white.svg`, and `icon-512x512-maskable.png`.

## Make structured delivery derivative, not authoritative

Prefer the project's existing token or asset-manifest format when one exists. Do not introduce a second schema merely because machine-readable output is possible.

If interoperable design tokens are explicitly requested and the project has no established format, use the current stable Design Tokens Community Group format where it fits the data. Do not implement a preview or editor's draft as if it were stable. Tokens are appropriate for reusable design decisions such as color or typography; they are not a substitute for the approved vector artwork and should not encode logo path geometry by default.

When automation needs an asset manifest and the project has no format, keep it minimal and include only fields the consumer needs. Useful metadata can include asset path, role, approval/lifecycle status, derived-from master and version, locale or market, usage-rights or expiry constraints, and validation status. Reference the human-readable handoff for rationale rather than duplicating prose into machine data.

## Support localization deliberately

Verify that selected fonts cover every required script and document approved fallback families. Record licensing constraints for all deployed font files.

Do not assume Latin-specific casing, spacing, or line-height behavior applies to every language. Treat localized wordmarks, translated lockups, or RTL-specific compositions as separate variants requiring explicit approval when the artwork changes. Preserve the canonical master relationship across variants.

## Web integration

When authorized, place assets in the project's existing public/static location and use the project framework's normal path rules. Update favicon, Apple icon, manifest, and social metadata consistently. Make the primary favicon link canonical and version its URL when a previously cached icon needs replacement.

Do not assume a relative social image URL will be accepted by every crawler. Use an absolute public URL when a deployment domain is known; otherwise state that deployment configuration still needs to supply it. Verify current target-platform metadata and image requirements when browsing or official documentation is available; if not, record the assumptions used.

For Open Graph images, include `og:image:width`, `og:image:height`, and `og:image:alt` when the integration emits those images. Keep alternate-language metadata aligned with localized assets when the application actually serves localized social previews.
