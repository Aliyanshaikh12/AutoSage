---
name: Auto Sage Diagnostic Studio
colors:
  surface: '#f7f9fc'
  surface-dim: '#d8dadd'
  surface-bright: '#f7f9fc'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f7'
  surface-container: '#eceef1'
  surface-container-high: '#e6e8eb'
  surface-container-highest: '#e0e3e6'
  on-surface: '#191c1e'
  on-surface-variant: '#434655'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eff1f4'
  outline: '#737686'
  outline-variant: '#c3c6d7'
  surface-tint: '#0053db'
  primary: '#004ac6'
  on-primary: '#ffffff'
  primary-container: '#2563eb'
  on-primary-container: '#eeefff'
  inverse-primary: '#b4c5ff'
  secondary: '#5d5e64'
  on-secondary: '#ffffff'
  secondary-container: '#e2e2e9'
  on-secondary-container: '#63646a'
  tertiary: '#4e565d'
  on-tertiary: '#ffffff'
  tertiary-container: '#676e76'
  on-tertiary-container: '#eaf1fa'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b4c5ff'
  on-primary-fixed: '#00174b'
  on-primary-fixed-variant: '#003ea8'
  secondary-fixed: '#e2e2e9'
  secondary-fixed-dim: '#c5c6cd'
  on-secondary-fixed: '#191c20'
  on-secondary-fixed-variant: '#45474c'
  tertiary-fixed: '#dce3ec'
  tertiary-fixed-dim: '#c0c7d0'
  on-tertiary-fixed: '#151c23'
  on-tertiary-fixed-variant: '#40484f'
  background: '#f7f9fc'
  on-background: '#191c1e'
  surface-variant: '#e0e3e6'
typography:
  display-hero:
    fontFamily: Inter
    fontSize: 40px
    fontWeight: '800'
    lineHeight: 48px
    letterSpacing: -0.03em
  headline-lg:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: 0em
  label-caps:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.08em
  telemetry-value-lg:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.03em
  telemetry-value-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '700'
    lineHeight: 24px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 22px
    fontWeight: '700'
    lineHeight: 28px
    letterSpacing: -0.02em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.25rem
  margin: 1.5rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system delivers an executive-grade automotive telemetry and diagnostic experience. It pairs the high-precision clarity of aviation glass-cockpit instrumentation with the ergonomic polish of contemporary electric vehicle operating systems. Built for automotive service engineers, diagnostic technicians, and fleet telematics managers, the visual architecture instills trust, rapid fault comprehension, and surgical precision under demanding workshop and control-room environments.

### Core Style Attributes
- **Technical Minimalism & Telemetry Density:** Clean, expansive white canvases offset by technical slate panels. Visual complexity is disciplined through spatial grid segregation and modular telemetry pods.
- **HUD Precision:** Sharp line icons, vector diagrams, and contextual diagnostic pins overlaid directly upon interactive digital twin surfaces.
- **Contrast Balancing:** High-contrast data highlights paired with quiet, structural neutral backdrops ensuring critical fault codes (DTCs) immediately capture operator attention without visual fatigue.
- **Spatial Elevation:** Diffused ambient luminescence, frosted sidebar navigation, and soft-radius container cards that frame complex mechanical diagnostics cleanly.

## Colors

The palette establishes an analytical diagnostic environment. The base interface employs an ultra-clean cool white-gray foundation (`#F3F5F8`), overlaid with pure white component cards (`#FFFFFF`) to maximize spatial depth and readability. Primary operations rely on vivid telemetry blue (`#2563EB`), supported by technical dark slate (`#24262B`) for deep hardware insight modules such as high-voltage battery schematics and real-time powertrain telemetry.

### Palette Architecture
- **Primary Telemetry (`#2563EB`):** Applied to active navigation indicators, key diagnostic triggers, selected states, and progressive telemetry gauges.
- **Deep Technical Carbon (`#24262B`):** Reserved for technical telemetry blocks, high-voltage battery inspection monitors, and terminal readouts. Provides high-contrast separation from the surrounding light dashboard.
- **Diagnostic Tints (`#EFF6FF`):** Backing fills for badges, AI telemetry capsules, and secondary interactive action regions.
- **Canvas Base (`#F3F5F8`):** Low-strain, neutral cool-gray structural bedrock behind modular cards.
- **Semantic Status Signals:**
  - *Nominal / Good:* `#10B981` (Emerald diagnostic clear)
  - *Warning / Attention:* `#F97316` (Amber caution, sensor anomalies)
  - *Critical Fault / Alert:* `#EF4444` (Brake, steering, high-voltage interlock breaches)
  - *AI / Automation:* `#3B82F6` to `#6366F1` (Neural processing indicators)
- **Text & Stroke Scale:**
  - *Headings & Primary Labels:* `#111827` (Deep neutral slate)
  - *Secondary Metrics & Metadata:* `#64748B` (Technical slate)
  - *Subtle Card Outlines:* `#E2E8F0` and `#F1F5F9`

## Typography

The type system is engineered around `Inter`, chosen for its pristine tabular numbers, vertical x-height consistency, and crisp rendering on dense high-DPI displays. Typography enforces immediate visual hierarchy: display labels use tracked uppercase formatting (`label-caps`) to categorize vehicle subsystems (e.g., `CAR ELECTRONICS`, `BATTERY`, `PRESSURE`), while live readouts and metric values leverage dense, bold glyphs to ensure scanning capability from standard diagnostic tablet distances.

### Typographic Rules
- **Diagnostic Section Headers:** Always rendered in uppercase tracking with `label-caps` (`letterSpacing: 0.08em`) to mimic vehicle instrumentation tags.
- **Metric Pairing:** Numerical readouts (`telemetry-value-lg` and `telemetry-value-md`) are consistently stacked above muted secondary descriptor labels in `body-sm`.
- **Status Pills & Chips:** Rendered using medium weight in `body-sm` with tight horizontal padding to preserve grid rhythm.

## Layout & Spacing

The layout structure employs a responsive multi-pane fluid grid framed by an ultra-slim vertical navigation rail (64px to 80px width) on the left margin. The main dashboard spans a responsive 12-column layout dividing the viewport into an expansive top stage (dedicated to the 3D digital vehicle twin and interactive sensor hotspots) and a bottom telemetry shelf containing modular diagnostic cards.

### Layout Mechanics
- **Desktop (1280px+):** Fixed left navigation rail, unified main workspace consisting of an upper 3D interactive stage and a multi-column modular grid for sensor feeds, powertrain telemetry, high-voltage battery monitor, and AI diagnostic assistant streams.
- **Tablet (768px - 1024px):** Navigation rail collapses to icons only; bottom telemetry cards collapse into a 2x2 grid below the vehicle digital twin canvas.
- **Mobile (<768px):** Navigation switches to a fixed bottom dock or off-canvas drawer. The 3D vehicle canvas adapts to touch rotation with vertical diagnostic cards scrolling in natural single-column flow.
- **Internal Density:** Component padding enforces a strict 16px (`space-md`) to 24px (`space-lg`) internal rhythm to maintain clean separation between critical sensor states.

## Elevation & Depth

Visual depth combines subtle planar stratification, soft ambient shadows, and micro-borders to maintain structural order without visual clutter. Surfaces interact on four distinct functional levels:

### Elevation Planes
- **Ground Floor (Base Canvas - `#F3F5F8`):** The primary host surface upon which all workspace containers rest.
- **Level 1 (Telemetry Cards & Digital Twin Stage - `#FFFFFF`):** High-efficiency white surfaces elevated with a subtle outline (`1px solid #E2E8F0`) and an ambient, low-density diffuse shadow (`box-shadow: 0 4px 20px -2px rgba(16, 24, 40, 0.04), 0 2px 6px -1px rgba(16, 24, 40, 0.02)`).
- **Level 2 (Technical Sub-Modules & Dark Knowledge Panels - `#24262B`):** Dark slate surface tier used for battery diagnostics and deep hardware architecture analysis. Features internal micro-borders (`1px solid rgba(255, 255, 255, 0.08)`) and inset drop shadows for tactile depth.
- **Level 3 (HUD Pins, Overlays & Floating Actions):** Floating callout chips (e.g., `Brakes Issue`, `AI Report`, hotspot telemetry tags) casting elevated, directional drop shadows (`box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.15), 0 8px 10px -6px rgba(0, 0, 0, 0.05)`).

## Shapes

The design system uses a refined, rounded geometric language (`roundedness: 2`). Standard telemetry containers, interactive metric cards, and vehicle stage modules feature `16px` (`rounded-lg`) corner radii, generating a smooth, contemporary industrial silhouette. Smaller controls such as buttons, tags, chips, and HUD pins utilize `8px` (`rounded-md`) to full pill radii (`9999px`) for quick tactile scanning.

### Geometry Specifications
- **Dashboard Containers & Large Modules:** `16px` to `24px` border radius (`rounded-lg` / `rounded-xl`).
- **Interactive Action Pills (e.g., AI Analyzes, Hotspot Badges):** `9999px` full pill radius.
- **Data Sub-Pills & Diagnostic Metrics:** `8px` to `12px` border radius.
- **Sidebar & Floating Action Buttons:** `12px` to `14px` border radius with smooth squircle curvature.

## Components

### Buttons & Interactive Controls
- **Primary CTA (`AI Analyzes`):** Filled primary blue (`#2563EB`) pill with crisp white text (`Inter 14px SemiBold`), paired with animated loading ringlets or status dots.
- **Secondary & Tertiary Buttons:** Pure white cards with subtle `#E2E8F0` border, muted text, and active elevation states on hover.
- **Floating HUD Pin Triggers:** Pill-shaped capsules with dual icon-label indicators, floating above 3D models with high-contrast warning or info colorways.

### Diagnostic Cards & Pods
- **White Telemetry Pod:** Standard container with `#FFFFFF` background, `16px` border radius, subtle `#E2E8F0` border, featuring upper label tags and centered graphical instrumentation (e.g., tire pressure bars, voltage radial dials, motor waveform plots).
- **Dark Telemetry Pod (`Battery / Inverter`):** `#24262B` background with subtle white line dividers, high-contrast white readout metrics (`93%`), integrated green health indicators (`Condition: Good`), and translucent schematic renders.

### Sensor Chips & Hotspot Indicators
- **Status Indicator Pods:** Vertically oriented sensor status blocks (e.g., `Camera`, `Pressure`, `Navigation`, `Radar`) paired with color-coded vertical cylinder gauges (blue for nominal, orange for alert) and action links (`Create report`).
- **HUD Hotspot Anchors:** Concentric glowing target pins (`#2563EB` and `#F97316`) positioned over 3D assemblies, triggering floating detail drawers on interaction.

### AI Diagnostic Assistant Panel
- Clean chat and reasoning stream container with soft badge avatars, real-time typing indicators (`Thinking...`), action control buttons (`Stop`), and inline solution recommendations.

### Navigation Rail & Global Controls
- Narrow left navigation dock with smooth inactive icons (`#94A3B8`) and active state pill highlights (`#2563EB` background with white icon).
- Top bar containing vehicle model selector dropdown, view mode toggles (`360° view mode`), omni-search input pill, and user profile badge.