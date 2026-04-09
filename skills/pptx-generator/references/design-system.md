# Design System

## Color Palette Reference

| # | Name | Colors | Style | Use Cases | Tips |
|---|------|--------|-------|-----------|------|
| 1 | Modern & Wellness | `#006d77` `#83c5be` `#edf6f9` `#ffddd2` `#e29578` | Fresh, soothing | Healthcare, counseling, skincare, yoga/spa | Deep teal for titles, light pink for background |
| 2 | Business & Authority | `#2b2d42` `#8d99ae` `#edf2f4` `#ef233c` `#d90429` | Formal, classic | Annual reports, financial analysis, corporate intro, government | Deep blue for professionalism, bright red to highlight data |
| 3 | Nature & Outdoors | `#606c38` `#283618` `#fefae0` `#dda15e` `#bc6c25` | Grounded, earthy | Outdoor gear, environmental, agriculture, historical culture | Dark green base, cream text |
| 4 | Vintage & Academic | `#780000` `#c1121f` `#fdf0d5` `#003049` `#669bbc` | Classic, scholarly | Academic lectures, history reviews, museums, heritage brands | Strong contrast between deep red and deep blue |
| 5 | Soft & Creative | `#cdb4db` `#ffc8dd` `#ffafcc` `#bde0fe` `#a2d2ff` | Dreamy, candy-toned | Mother & baby, desserts, women's fashion, kindergarten | Use dark gray or black for text |
| 6 | Bohemian | `#ccd5ae` `#e9edc9` `#fefae0` `#faedcd` `#d4a373` | Gentle, muted | Wedding planning, home decor, organic food, slow living | Cream background, green-brown accents |
| 7 | Vibrant & Tech | `#8ecae6` `#219ebc` `#023047` `#ffb703` `#fb8500` | High energy, sporty | Sports events, gyms, startup pitches, youth education | Deep blue for stability, orange as focal accent |
| 8 | Craft & Artisan | `#7f5539` `#a68a64` `#ede0d4` `#656d4a` `#414833` | Rustic, coffee-toned | Coffee shops, handicrafts, traditional culture, bakery | Suited for paper/leather textures |
| 9 | Tech & Night | `#000814` `#001d3d` `#003566` `#ffc300` `#ffd60a` | Deep, luminous | Tech launches, astronomy, night economy, luxury automobiles | Must use dark mode |
| 10 | Education & Charts | `#264653` `#2a9d8f` `#e9c46a` `#f4a261` `#e76f51` | Clear, logical | Statistical reports, education, market analysis, general business | Perfect chart color scheme |
| 11 | Forest & Eco | `#dad7cd` `#a3b18a` `#588157` `#3a5a40` `#344e41` | Monochrome gradient, forest | Landscape design, ESG reports, environmental causes, botanical | Monochrome palette is safe and cohesive |
| 12 | Elegant & Fashion | `#edafb8` `#f7e1d7` `#dedbd2` `#b0c4b1` `#4a5759` | Muted, Morandi tones | Haute couture, art galleries, beauty brands, magazine style | Negative space is key |
| 13 | Art & Food | `#335c67` `#fff3b0` `#e09f3e` `#9e2a2b` `#540b0e` | Rich, vintage-poster | Food documentaries, art exhibitions, ethnic themes, vintage restaurants | Works well with large color blocks |
| 14 | Luxury & Mysterious | `#22223b` `#4a4e69` `#9a8c98` `#c9ada7` `#f2e9e4` | Cool, purple-toned | Jewelry showcases, hotel management, high-end consulting, psychology | Purple evokes premium atmosphere |
| 15 | Pure Tech Blue | `#03045e` `#0077b6` `#00b4d8` `#90e0ef` `#caf0f8` | Futuristic, clean | Cloud/AI, water/ocean, hospitals, clean energy | Deep ocean to sky gradient |
| 16 | Coastal Coral | `#0081a7` `#00afb9` `#fdfcdc` `#fed9b7` `#f07167` | Refreshing, summery | Travel, summer events, beverage brands, ocean themes | Teal and coral as complementary focal colors |
| 17 | Vibrant Orange Mint | `#ff9f1c` `#ffbf69` `#ffffff` `#cbf3f0` `#2ec4b6` | Bright, cheerful | Children's events, promotional posters, FMCG, social media | Orange grabs attention, mint feels fresh |
| 18 | Platinum White Gold | `#0a0a0a` `#0070F3` `#D4AF37` `#f5f5f5` `#ffffff` | Premium, professional | Agent products, corporate websites, fintech, luxury brands | White-gold base, blue for action, gold for emphasis |

---

## Color Palette Rules (MANDATORY)

### Strict Palette Adherence

**Use ONLY the provided color palette. Do NOT create or modify colors.**

- All colors must come from the user-provided palette
- Do NOT use colors outside the palette
- Do NOT modify palette colors (brightness, saturation, mixing)
- **Only exception**: Add transparency using the `transparency` property (0-100)

```javascript
// Correct: Using palette colors
slide.addShape(pres.shapes.RECTANGLE, { fill: { color: theme.primary } });
slide.addText("Title", { color: theme.accent });

// Wrong: Colors outside palette
slide.addShape(pres.shapes.RECTANGLE, { fill: { color: "1a1a2e" } });
```

### No Gradients

**Gradients are prohibited. Use solid colors only.**

### No Animations

**Animations and transitions are prohibited.** All slides must be static.

---

## Font Reference

### Recommended Fonts

| Language | Default Font | Alternatives |
|----------|-------------|--------------|
| **Chinese** | Microsoft YaHei | — |
| **English** | Arial | Georgia, Calibri, Cambria, Trebuchet MS |

### Recommended Font Pairings

| Header Font | Body Font |
|-------------|-----------|
| Georgia | Calibri |
| Arial Black | Arial |
| Calibri | Calibri Light |
| Cambria | Calibri |
| Trebuchet MS | Calibri |
| Impact | Arial |
| Palatino | Garamond |
| Consolas | Calibri |

### No Bold for Body Text

**Plain body text and caption/legend text must NOT use bold.**

- Body paragraphs, descriptions → normal weight
- Captions, legends, footnotes → normal weight
- Reserve bold for titles and headings only

---

## Style Recipes

| Style | Corner Radius | Spacing | Best For |
|-------|--------------|---------|----------|
| **Sharp & Compact** | 0 ~ 0.05" | Tight | Data-dense, tables, professional reports |
| **Soft & Balanced** | 0.08" ~ 0.12" | Moderate | Corporate, business presentations, general use |
| **Rounded & Spacious** | 0.15" ~ 0.25" | Relaxed | Product intros, marketing, creative showcases |
| **Pill & Airy** | 0.3" ~ 0.5" | Open | Brand showcases, launch events, premium presentations |

### Sharp & Compact

| Category | Value (inches) | Notes |
|----------|---------------|-------|
| Corner radius — small | 0" | Full right angle |
| Corner radius — medium | 0.03" | Micro-rounded |
| Corner radius — large | 0.05" | Slight rounding |
| Element padding | 0.1" ~ 0.15" | Compact |
| Element gap | 0.1" ~ 0.2" | Compact |
| Page margin | 0.3" | Narrow |

### Soft & Balanced

| Category | Value (inches) | Notes |
|----------|---------------|-------|
| Corner radius — small | 0.05" | Slight rounding |
| Corner radius — medium | 0.08" | Medium rounding |
| Corner radius — large | 0.12" | Larger rounding |
| Element padding | 0.15" ~ 0.2" | Moderate |
| Element gap | 0.15" ~ 0.25" | Moderate |
| Page margin | 0.4" | Standard |

### Rounded & Spacious

| Category | Value (inches) | Notes |
|----------|---------------|-------|
| Corner radius — small | 0.1" | Medium rounding |
| Corner radius — medium | 0.15" | Large rounding |
| Corner radius — large | 0.25" | Very large rounding |
| Element padding | 0.2" ~ 0.3" | Relaxed |
| Element gap | 0.25" ~ 0.4" | Relaxed |
| Page margin | 0.5" | Wide |

### Pill & Airy

| Category | Value (inches) | Notes |
|----------|---------------|-------|
| Corner radius — small | 0.2" | Large rounding |
| Corner radius — medium | 0.3" | Pill shape |
| Corner radius — large | 0.5" | Full pill |
| Element padding | 0.25" ~ 0.4" | Open |
| Element gap | 0.3" ~ 0.5" | Open |
| Page margin | 0.6" | Wide |

### Quick Selection Guide

| Presentation Type | Recommended Style | Reason |
|------------------|------------------|--------|
| Finance / Data reports | Sharp & Compact | High density, serious and precise |
| Corporate / Business | Soft & Balanced | Balances professionalism and approachability |
| Product intro / Marketing | Rounded & Spacious | Modern feel, friendly |
| Launch events / Brand | Pill & Airy | Premium feel, visual impact |
| Training / Education | Soft / Rounded | Clear, readable, friendly |
| Tech sharing | Sharp / Soft | Professional, information-dense |

---

## Typography Scale (PPT)

| Usage | Size (pt) | Notes |
|-------|-----------|-------|
| Annotations / Sources | 10 ~ 12 | Minimum readable size |
| Body / Description | 14 ~ 16 | Standard body |
| Subtitle | 18 ~ 22 | Secondary heading |
| Title | 28 ~ 36 | Page title |
| Large Title | 44 ~ 60 | Cover / section title |
| Data Callout | 60 ~ 96 | Key number display |

## Spacing Scale (PPT)

Based on 10" x 5.625" slide dimensions:

| Usage | Recommended (inches) |
|-------|---------------------|
| Icon-to-text gap | 0.08" ~ 0.15" |
| List item spacing | 0.15" ~ 0.25" |
| Card inner padding | 0.2" ~ 0.4" |
| Element group gap | 0.3" ~ 0.5" |
| Page safe margin | 0.4" ~ 0.6" |
| Major block gap | 0.5" ~ 0.8" |
