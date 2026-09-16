---
name: Oceanic Intelligence
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#3d4947'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#6d7a77'
  outline-variant: '#bcc9c6'
  surface-tint: '#006a61'
  primary: '#00685f'
  on-primary: '#ffffff'
  primary-container: '#008378'
  on-primary-container: '#f4fffc'
  inverse-primary: '#6bd8cb'
  secondary: '#565e74'
  on-secondary: '#ffffff'
  secondary-container: '#dae2fd'
  on-secondary-container: '#5c647a'
  tertiary: '#006194'
  on-tertiary: '#ffffff'
  tertiary-container: '#007bb9'
  on-tertiary-container: '#fdfcff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#89f5e7'
  primary-fixed-dim: '#6bd8cb'
  on-primary-fixed: '#00201d'
  on-primary-fixed-variant: '#005049'
  secondary-fixed: '#dae2fd'
  secondary-fixed-dim: '#bec6e0'
  on-secondary-fixed: '#131b2e'
  on-secondary-fixed-variant: '#3f465c'
  tertiary-fixed: '#cce5ff'
  tertiary-fixed-dim: '#93ccff'
  on-tertiary-fixed: '#001d31'
  on-tertiary-fixed-variant: '#004b73'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: -0.005em
  body-lg:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
  body-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 16px
  label-md:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.04em
  label-sm:
    fontFamily: Inter
    fontSize: 10px
    fontWeight: '600'
    lineHeight: 12px
    letterSpacing: 0.06em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1rem
  margin: 1.5rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1rem
  space-xl: 1.5rem
---

## Brand & Style

The design system establishes a high-precision, mission-critical workspace tailored for maritime operators, environmental scientists, coast guards, and compliance analysts. The interface prioritizes calm authority, optical clarity, and uninterrupted situational awareness. Rather than presenting speculative or futuristic visuals, it relies on grounded, institutional enterprise design patterns engineered for prolonged operational shifts.

Key tenants of the aesthetic approach:
- **Utilitarian Discipline:** Every pixel, border, and pixel offset exists to clarify complex spatial and telemetry data.
- **Enterprise Restraint:** Pure functional hierarchy with zero non-standard visual treatments such as glowing accents, excessive gradients, or frosted glass blurs.
- **Contextual Anchoring:** Dark structural frames (sidebars, toolbars) secure the visual boundaries, while luminous, high-contrast work surfaces maximize legibility for charts, AIS tracks, and dense analytical tables.

## Colors

The color architecture enforces a high-contrast division between structural workspace framing, informational content backdrops, and operational signal alerts.

### Palette Architecture
- **Primary (Maritime Teal - `#0D9488`):** The primary interaction anchor, reserved strictly for focal actions, interactive states, selected map entities, and confirmed positive attributions. Deeper tone `#0F766E` serves hover/active states, while `#14B8A6` is reserved for fine-detail indicators against dark panels.
- **Secondary (Deep Nautical Slate - `#0F172A` & `#1E293B`):** Forms persistent global structures, including primary navigational rails, status headers, and contextual map overlays.
- **Surfaces & Grounds:**
  - Base canvas: `#F1F5F9` (cool, eye-resting light grey slate).
  - Raised panels & workspace cards: `#FFFFFF`.
  - Secondary wells and table header fills: `#F8FAFC`.
  - Perimeter dividers: `#E2E8F0`.
- **System Telemetry & State Colors:**
  - *Active / Critical:* Crimson alert (`#DC2626` text, `#FEF2F2` fill, `#FCA5A5` stroke).
  - *Under Review / Warning:* Amber amber (`#D97706` text, `#FFFBEB` fill, `#FCD34D` stroke).
  - *Resolved / Stable:* Emerald green (`#16A34A` text, `#F0FDF4` fill, `#86EFAC` stroke).
  - *Confidence Levels:* High (`#0D9488`), Medium (`#0284C7`), Low (`#64748B`).

## Typography

The typography is built entirely on `Inter` to deliver systematic clarity, tabular alignment, and zero ambiguity between numerical characters. 

- **Numerical & Coordinate Precision:** For table columns representing coordinates (Latitude/Longitude), MMSI/IMO registration numbers, knots, and UTC timestamps, tabular figures (`font-variant-numeric: tabular-nums`) are strictly enforced.
- **Information Hierarchy:** Section headers, table labels, and telemetry descriptors favor structural weight (SemiBold/Medium) at compact optical sizes over oversized headings, protecting screen real estate for maps and data views.
- **Micro-Labels:** Metadata identifiers (`label-md`, `label-sm`) use uppercase treatments with expanded letter spacing to ensure immediate scannability when framing telemetry tags.

## Layout & Spacing

The layout is built for expansive desktop monitoring configurations (1440px wide and above), operating under a structural panel framework rather than a generic promotional document flow.

- **Canvas Organization:** A rigid shell comprising a collapsed/expanded deep navy utility rail (width: 64px to 240px), an operational top status utility bar (height: 48px), and dynamic multi-split viewports (flexible map tiles, telemetry sidebars, split-pane tables).
- **Rhythm & Padding:** Densities follow an 8px grid with 4px sub-increments for compact telemetry readouts. Data grids and form assemblies utilize `space-sm` (8px) and `space-md` (12px) padding to preserve analytical density without producing visual crowding.
- **Card Containers:** Distinct information surfaces use `space-lg` (16px) for interior padding, cleanly bound by structural borders to isolate critical incident fields.

## Elevation & Depth

Visual hierarchy is managed through clean tonal differentiation, precise structural borders, and subtle, physical ambient shadows. Diffused glows and unnatural blurs are prohibited.

- **Level 0 (App Shell & Canvas):** Tone `#F1F5F9` with no elevation.
- **Level 1 (Data Cards, Panels, Table Blocks):** Flat `#FFFFFF` surface contained by a sharp 1px border (`#E2E8F0`) and reinforced by a subtle natural drop shadow: `0 1px 3px 0 rgba(15, 23, 42, 0.05), 0 1px 2px -1px rgba(15, 23, 42, 0.05)`.
- **Level 2 (Popovers, Filter Menus, Map HUD Overlays):** `#FFFFFF` with 1px border (`#CBD5E1`) and moderate natural shadow: `0 4px 6px -1px rgba(15, 23, 42, 0.07), 0 2px 4px -2px rgba(15, 23, 42, 0.05)`.
- **Level 3 (Modals, Spill Attribution Confirmation Dialogs):** Centered `#FFFFFF` structure accompanied by a pure dark navy backdrop scrim (`#0F172A` at 45% opacity) and an extended shadow: `0 10px 15px -3px rgba(15, 23, 42, 0.1), 0 4px 6px -4px rgba(15, 23, 42, 0.05)`.

## Shapes

The design system employs a disciplined, professional shape standard (`roundedness: 1` - Soft). 

- **Cards, Panels, & Map Modals:** Fixed corner radius of 4px (`0.25rem`) to 6px. This maintains sharp, structured boundaries across dense operational displays.
- **Form Controls & Inputs:** 4px radius, preserving clean geometric alignment when stacked adjacent to tabular lists and side-by-side inspect panels.
- **Status Pills & Chips:** 4px subtle rounded boxes (never pill or stadium curves), preventing an overly informal appearance and maintaining consistent enterprise proportions across table lines.

## Components

### Buttons
- **Primary:** Background `#0D9488`, text `#FFFFFF`, 1px border `transparent`, subtle natural shadow. Hover: `#0F766E`. Active: `#115E59`.
- **Secondary:** Background `#FFFFFF`, text `#0F172A`, 1px border `#CBD5E1`. Hover: `#F8FAFC`, border `#94A3B8`.
- **Destructive:** Background `#DC2626`, text `#FFFFFF`. Hover: `#B91C1C`.
- **Ghost/Icon:** Background `transparent`, text `#475569`. Hover: `#F1F5F9`, text `#0F172A`.

### Status Badges & Chips
Badges use 4px corner radii, a 1px border, and uppercase `label-sm` typography:
- **Active Spill:** Fill `#FEF2F2`, border `#FECACA`, text `#DC2626`.
- **Under Review:** Fill `#FFFBEB`, border `#FDE68A`, text `#D97706`.
- **Resolved:** Fill `#F0FDF4`, border `#BBF7D0`, text `#16A34A`.
- **Confidence Metrics:** Low (Slate `#64748B`), Medium (Sky `#0284C7`), High (Teal `#0D9488`). Rendered as paired key-value indicators.

### Data Tables
- **Header:** Background `#F8FAFC`, height 36px, typography `label-md`, text `#475569`, bottom border 1px solid `#E2E8F0`.
- **Rows:** Background `#FFFFFF`, alternating/hover state `#F8FAFC`, minimum height 40px, inline cell padding 12px, bottom border 1px solid `#F1F5F9`.
- **Data Display:** Numerical values, coordinates, and vessel callsigns strictly aligned with monospaced tabular numbers.

### Inputs & Controls
- **Form Fields:** Height 34px, background `#FFFFFF`, border 1px solid `#CBD5E1`, text `#0F172A`, placeholder `#94A3B8`. Focus state: border `#0D9488` with a 1px outer ring `rgba(13, 148, 136, 0.2)`.
- **Checkboxes & Radios:** 16px square/circle, border 1px solid `#94A3B8`, active fill `#0D9488`.

### Map Information Containers
- Floating HUD cards over map viewports leverage Level 2 elevation, `#FFFFFF` opaque background, 1px border `#E2E8F0`, and compact header bars with nautical slate title text to display live AIS metrics, slick volume estimations, and trajectory drift projections.