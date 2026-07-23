# Notes: editing JE proposal .docx files programmatically

These are patterns and gotchas accumulated from editing Johnston Engineering proposal Word
documents in past sessions. **This file is notes, not a tool** — it doesn't include any
document-editing scripts. See README.md for why, and for what to set up instead.

## Two viable approaches

1. **Surgical XML editing** — unpack the .docx as a zip, edit `word/document.xml` directly with
   targeted find/replace, then repack and validate. Good for small, precise edits to an existing
   proposal (e.g., fixing one paragraph, updating one price).
2. **Programmatic build** — generate the .docx from scratch or near-scratch using a Node.js
   library (e.g., the `docx` npm package). Better for building new proposals section-by-section
   from the standards in `CLAUDE.md`.

Whichever tool you set up in Claude Code (see README), expect to render to PDF and rasterize
pages to visually check formatting before calling an edit "done" — Word XML edits that look
correct in the markup can still render incorrectly (page breaks, spacing, table splits).

## Gotchas specific to JE proposal documents

- **Narrow no-break spaces:** Word inserts `\u202F` (narrow no-break space) between numbers and
  units throughout the XML — e.g. "≈ 32 labor hours" or "5–10 kW". A long string replacement
  targeting that exact phrase will silently fail to match. Fix by targeting only ASCII-safe
  changed words, or by anchor-extraction (find start/end positions, replace the slice) instead
  of a literal string match.
- **`docx`-library table borders:** if generating tables with the `docx` npm library, it emits
  `<w:pBdr>` border child elements in the wrong schema order (top, bottom, left, right instead of
  the required top, left, bottom, right). Fix by post-processing the packed .docx zip with a
  regex reorder of the `pBdr` children before delivering the file.
- **Paragraph IDs:** any inserted paragraph needs a `w14:paraId` in a valid range, or Word will
  show a "needs repair" prompt on open. Don't reuse `0` or out-of-range values.
- **Page breaks:** `pageBreakBefore: true` on a paragraph gives a clean hard page break before a
  section heading.
- **`keepNext`:** chains paragraphs together so they can't be split across a page break — useful
  for headings + their first line, but over-applying it across a whole section pushes the whole
  group to the next page and creates large blank spaces. Use selectively.
- **Table row splitting:** `cantSplit: true` on a `TableRow` prevents that row breaking across
  pages; `tableHeader: true` makes header rows repeat when a table spans multiple pages. Useful
  together for the Cost Summary and Baseline Hardware List tables.
- **File extensions can lie:** some project files with a `.docx` extension turn out to be plain
  text and readable with `cat`. Some `.pdf` files turn out to be zip archives containing
  per-page JPEGs plus extracted text, readable by unzipping directly. Check before assuming a
  binary parser is needed.

## Validation workflow (regardless of tool)

1. Edit.
2. Convert to PDF (e.g., via LibreOffice headless).
3. Rasterize a few pages to JPEG at ~72–90 DPI.
4. Visually check the pages that changed, and the page before/after them for reflow effects.
5. Only then call it done.
