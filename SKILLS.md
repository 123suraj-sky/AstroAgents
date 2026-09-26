# Installed Kiro Skills

All skills are located in `.kiro/skills/`. Each skill is a SKILL.md file that Kiro loads on demand to bring specialized knowledge into context.

> **Total:** 27 skills installed across two collections.

---

## Animation & Motion (Emil Kowalski)

Skills from [emilkowalski/skills](https://github.com/emilkowalski/skills) — opinionated, craft-driven animation and UI philosophy.

| Folder | Skill Name | Size | Description |
|---|---|---|---|
| `animate` | `animate` | 11.6 KB | Build a web animation from scratch — decides whether it should animate, picks the tool, curve, duration, interruption and exit. Writes the implementation. Use for any "add motion" or "make this feel alive" task. For critiquing existing motion use `review-animations`; for auditing a codebase use `improve-animations`. |
| `animate-expo` | `animate-expo` | 17.5 KB | Build animations in React Native and Expo — which thread it runs on, spring or timing, gesture handoff, how it degrades. Implements with Reanimated, Gesture Handler, Expo Router, and expo-haptics. For web animation use `animate`. |
| `animation-vocabulary` | `animation-vocabulary` | 13.1 KB | Reverse-lookup glossary that turns a vague motion description into its exact term ("the bouncy thing when a popover opens" → Pop in; "the iOS rubber-band scroll" → Rubber-banding). For naming an effect, not designing or building one. |
| `apple-design` | `apple-design` | 22.5 KB | Apple's approach to fluid, physical interface design translated for the web — spring animations, gesture-driven UI, drag/swipe/sheet interactions, momentum, interruptible transitions, translucent materials, typography (optical sizing, tracking, leading), and reduced-motion. |
| `ask-sonner` | `ask-sonner` | 7.1 KB | Complete guide to Sonner, the React toast library — install, wire up the Toaster, pick the right `toast()` call, promise and loading toasts, updating, dismissing, styling, theming, icons, positioning, and troubleshooting (toasts not appearing, appearing twice, ignoring Tailwind, sitting behind a modal). |
| `emil-design-eng` | `emil-design-eng` | 26.5 KB | Encodes Emil Kowalski's complete philosophy on UI polish, component design, animation decisions, and the invisible details that make software feel great. |
| `find-animation-opportunities` | `find-animation-opportunities` | 9.6 KB | Sweeps a codebase or UI for places that don't animate but should, and rejects everything that shouldn't. Read-only — proposes motion with exact values, does not implement. Use when asking "what could be animated here?" or wanting to "make this feel more alive". |
| `impeccable` | `impeccable` | 11.6 KB | Use when designing, redesigning, critiquing, auditing, or polishing any frontend interface — websites, dashboards, product UI, components, forms, onboarding, and empty states. Covers UX review, visual hierarchy, accessibility, responsive behavior, theming, typography, spacing, color, motion, and design systems. |
| `improve-animations` | `improve-animations` | 8.0 KB | Surveys a codebase's animation and motion code as a senior motion advisor, then produces a prioritized audit and self-contained implementation plans for other agents or models to execute. Read-only on source — it plans improvements, not applies them. |
| `mobile-native` | `mobile-native` | 16.4 KB | Makes a web app feel native on a phone — CSS and meta-tag fixes for sticky hover states, tap highlight flashes, the 100vh bug, inputs that zoom the page, laggy taps, pull-to-refresh, content under the notch, long-press text selection, carousel scroll direction, and mismatched status bars. For motion use `animate`; for React Native use `animate-expo`. |
| `pick-ui-library` | `pick-ui-library` | 4.7 KB | Picks the right library for a frontend task from a curated, opinionated list — numbers, OTP inputs, charts, command menus, virtualization, drag and drop, toasts, state, styling, and more. Only runs when explicitly invoked. |
| `prototype` | `prototype` | 7.7 KB | Builds multiple genuinely different versions of a UI piece behind a visual picker so you can flip through them live and promote the winner. Only runs when explicitly invoked. |
| `review-animations` | `review-animations` | 8.2 KB | Reviews animation and motion code against a high craft bar derived from Emil Kowalski's design engineering philosophy. Default to flagging; approval is earned. |
| `write-swift` | `write-swift` | 41.4 KB | How to write modern Swift well — value types, Swift 6 data-race safety, approachable concurrency (`@concurrent`, main-actor-by-default, actors, task groups), protocols and generics (`some` vs `any`), API design, performance and ARC, Swift Testing, macros, and modern language features. Use when writing, reviewing, or migrating Swift, or fixing concurrency errors, hangs, data races, or retain cycles. |

---

## Frontend Design & Visual Taste (LeonxlNx / taste-skill)

Skills from [LeonxlNx/taste-skill](https://github.com/LeonxlNx/taste-skill) — anti-slop, agency-level UI design and image generation.

| Folder | Skill Name | Size | Description |
|---|---|---|---|
| `brandkit` | `brandkit` | 13.5 KB | Premium brand-kit image generation — brand-guidelines boards, logo systems, identity decks, and visual-world presentations. Covers minimalist, cinematic, editorial, dark-tech, luxury, cultural, security, gaming, and developer-tool brand systems. |
| `brutalist-skill` | `industrial-brutalist-ui` | 8.3 KB | Raw mechanical interfaces fusing Swiss typographic print with military terminal aesthetics. Rigid grids, extreme type scale contrast, utilitarian color, analog degradation effects (halftones, CRT scanlines, bitmap dithering). For data-heavy dashboards, portfolios, or editorial sites that should feel like declassified blueprints. |
| `gpt-tasteskill` | `gpt-taste` | 7.7 KB | Awwwards-level design engineering — Python-driven layout randomization, strict AIDA page structure, wide editorial typography (bans 6-line hero wraps), gapless bento grids, GSAP ScrollTriggers (pinning, stacking, scrubbing), inline micro-images, and massive section spacing. |
| `image-to-code-skill` | `image-to-code` | 35.8 KB | Elite image-to-code skill for Codex — generates design images first, deeply analyzes them, then implements the website to match. Prefers large section-specific images over tiny compressed boards, avoids cards-inside-cards UI, and keeps the hero clean and visible on a small laptop. |
| `imagegen-frontend-mobile` | `imagegen-frontend-mobile` | 39.5 KB | Elite mobile app image-generation — premium app-native screen concepts and flows for iOS, Android, and cross-platform. Prioritizes clean hierarchy, readable text, multi-screen consistency, controlled palettes, non-generic art direction, textured surfaces, and clean phone mockup framing. Generates images only, does not write code. |
| `imagegen-frontend-web` | `imagegen-frontend-web` | 36.2 KB | Elite frontend image-direction — generates one separate horizontal image per website section (8 sections = 8 images, never compressed into one). Enforces composition variety, background-image freedom, varied CTAs, varied hero scales, a narrative concept spine, and a single consistent palette. |
| `minimalist-skill` | `minimalist-ui` | 7.7 KB | Clean editorial-style interfaces — warm monochrome palette, typographic contrast, flat bento grids, muted pastels. No gradients, no heavy shadows. Bans Inter, Lucide icons, default Tailwind shadows, and AI copywriting clichés. |
| `output-skill` | `full-output-enforcement` | 2.5 KB | Overrides default LLM truncation behavior — enforces complete code generation, bans all placeholder patterns (`// ...`, `// rest of code`, "for brevity"), and handles token-limit splits cleanly with a `[PAUSED]` marker. Apply to any task requiring exhaustive, unabridged output. |
| `redesign-skill` | `redesign-existing-projects` | 14.7 KB | Upgrades existing websites and apps to premium quality — audits current design, identifies generic AI patterns across typography, color, layout, interactivity, content, components, and iconography, then applies targeted fixes without breaking functionality. Works with any CSS framework or vanilla CSS. |
| `soft-skill` | `high-end-visual-design` | 10.3 KB | Teaches agency-level UI design — exact fonts, spacing, shadows, card structures (Double-Bezel / Doppelrand architecture), and animations that make a website feel expensive. Blocks all common defaults that make AI designs look cheap. |
| `stitch-skill` | `stitch-design-taste` | 11.6 KB | Semantic Design System Skill for Google Stitch — generates agent-friendly `DESIGN.md` files that enforce premium, anti-generic UI standards: strict typography, calibrated color, asymmetric layouts, perpetual micro-motion, and hardware-accelerated performance. |
| `taste-skill` | `design-taste-frontend` | 85.5 KB | The main anti-slop frontend skill for landing pages, portfolios, and redesigns — reads the brief, infers the right design direction, sets three dials (Variance / Motion / Density), maps to the correct design system, and ships interfaces that don't look templated. Includes a full pre-flight check and strict anti-pattern rules. |
| `taste-skill-v1` | `design-taste-frontend-v1` | 20.7 KB | The original v1 taste-skill, preserved for backward compatibility. Use only when a project depends on its exact behavior. The current default is `taste-skill` (v2). |

---

## Quick Reference

| When you want to… | Use skill |
|---|---|
| Add animation to a web component | `animate` |
| Add animation to a React Native / Expo app | `animate-expo` |
| Name a motion effect you've seen | `animation-vocabulary` |
| Build Apple-style fluid, gesture-driven UI on web | `apple-design` |
| Work with Sonner toasts | `ask-sonner` |
| Apply Emil's full UI polish philosophy | `emil-design-eng` |
| Find where a UI should (and shouldn't) animate | `find-animation-opportunities` |
| Polish or critique any frontend interface | `impeccable` |
| Audit and plan animation improvements across a codebase | `improve-animations` |
| Make a web app feel native on mobile | `mobile-native` |
| Pick the right frontend library for a task | `pick-ui-library` |
| Build and compare multiple UI variants | `prototype` |
| Code-review animation changes | `review-animations` |
| Write modern Swift 6 | `write-swift` |
| Generate a brand identity board image | `brandkit` |
| Build a brutalist / industrial UI | `brutalist-skill` |
| Build Awwwards-level UI with GSAP | `gpt-tasteskill` |
| Design an image then implement it as code (Codex) | `image-to-code-skill` |
| Generate premium mobile app screen images | `imagegen-frontend-mobile` |
| Generate per-section website design reference images | `imagegen-frontend-web` |
| Build a clean minimalist editorial UI | `minimalist-skill` |
| Force complete, untruncated code output | `output-skill` |
| Upgrade an existing website to premium quality | `redesign-skill` |
| Build a high-end agency-level UI | `soft-skill` |
| Generate a DESIGN.md for Google Stitch | `stitch-skill` |
| Build a premium landing page, portfolio, or redesign | `taste-skill` |
| Use the original v1 taste-skill | `taste-skill-v1` |
