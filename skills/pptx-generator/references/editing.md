# Editing Existing Presentations

## Template-Based Workflow

When using an existing presentation as a template:

1. **Copy and analyze**:
   ```bash
   cp /path/to/user-provided.pptx template.pptx
   python -m markitdown template.pptx > template.md
   ```
   Review `template.md` to see placeholder text and slide structure.

2. **Plan slide mapping**: For each content section, choose a template slide.

   **USE VARIED LAYOUTS** — monotonous presentations are a common failure mode. Actively seek out:
   - Multi-column layouts (2-column, 3-column)
   - Image + text combinations
   - Full-bleed images with text overlay
   - Quote or callout slides
   - Section dividers
   - Stat/number callouts
   - Icon grids or icon + text rows

3. **Unpack**: Extract the PPTX into an editable XML tree using Python's `zipfile` module.

4. **Build presentation** (do this yourself, not with subagents):
   - Delete unwanted slides (remove from `<p:sldIdLst>`)
   - Duplicate slides you want to reuse
   - Reorder slides in `<p:sldIdLst>`
   - **Complete all structural changes before step 5**

5. **Edit content**: Update text in each `slide{N}.xml`.
   **Use subagents here if available** — slides are separate XML files.

6. **Clean**: Remove orphaned files.

7. **Pack**: Repack the XML tree into a PPTX file. Always write to `/tmp/` first.

## Output Structure

```
./
├── template.pptx               # Copy of user-provided file (never modified)
├── template.md                 # markitdown extraction
├── unpacked/                   # Editable XML tree
└── edited.pptx                 # Final repacked deck
```

## Formatting Rules

- **Bold all headers, subheadings, and inline labels**: Use `b="1"` on `<a:rPr>`
- **Never use unicode bullets**: Use proper list formatting with `<a:buChar>` or `<a:buAutoNum>`
- **Bullet consistency**: Let bullets inherit from the layout

## Common Pitfalls — Template Editing

### Multi-Item Content

If source has multiple items, create separate `<a:p>` elements for each — **never concatenate into one string**.

### Smart Quotes

Use XML entities:
| Character | Name | Unicode | XML Entity |
|-----------|------|---------|------------|
| " | Left double quote | U+201C | `&#x201C;` |
| " | Right double quote | U+201D | `&#x201D;` |

### Other

- **Whitespace**: Use `xml:space="preserve"` on `<a:t>` with leading/trailing spaces
- **XML parsing**: Use `defusedxml.minidom`, not `xml.etree.ElementTree` (corrupts namespaces)
