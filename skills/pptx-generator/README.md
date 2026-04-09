# PPTX Generator & Editor

Generate, edit, and read PowerPoint presentations with professional design.

## Features

- **Create from Scratch**: Full PPTX generation using PptxGenJS with cover, TOC, content, section divider, and summary slides
- **Edit Existing PPTX**: Template-based editing via XML manipulation
- **Read/Extract**: Text extraction from any .pptx file via markitdown
- **Design System**: 18 color palettes, 4 visual styles (Sharp/Soft/Rounded/Pill), font pairings
- **5 Slide Types**: Cover, Table of Contents, Section Divider, Content Page, Summary/Closing
- **Chinese Support**: Microsoft YaHei font for Chinese content

## Usage

### Trigger

- Say "做PPT", "生成PPT", "帮我做演示文稿"
- Say "create presentation", "make slides", "PPTX"

### Quick Start

```bash
# Install dependencies
npm install -g pptxgenjs
pip install "markitdown[pptx]"

# Read existing PPTX
python -m markitdown presentation.pptx
```

### Workflow

1. **Research** — understand topic, audience, purpose, tone
2. **Select palette & fonts** — from 18 color palettes in design-system.md
3. **Select style** — Sharp/Soft/Rounded/Pill
4. **Plan slides** — classify each slide as one of 5 types
5. **Generate JS files** — one per slide, using PptxGenJS
6. **Compile** — combine all slides into final .pptx
7. **QA** — verify with markitdown extraction

## Dependencies

- `npm install -g pptxgenjs` — PPTX creation
- `pip install "markitdown[pptx]"` — text extraction
- `npm install -g react-icons react react-dom sharp` — icons (optional)

## Directory Structure

```
pptx-generator/
├── SKILL.md                    # Skill instructions
├── manifest.json               # Skill metadata
├── README.md                   # This file
└── references/
    ├── slide-types.md          # 5 slide types + layout patterns
    ├── design-system.md        # Color palettes, fonts, style recipes
    ├── editing.md              # Template editing workflow
    ├── pitfalls.md             # QA process & common mistakes
    └── pptxgenjs.md            # PptxGenJS API reference
```

## Source

Original skill from [MiniMax-AI/skills](https://github.com/MiniMax-AI/skills). Adapted for AI Store Skill广场.
