# Workflow 14 — Win/loss calibration (tune the ICP model from outcomes)

Trigger: "calibrate the model", "win/loss review", "tune ICP from outcomes",
"what's actually converting", "recalibrate scoring"; periodic (quarterly) and
on-demand.

Closes the loop the pipeline otherwise leaves open: outcomes →
`scoring_taxonomy.json` → WF5 workbook scoring → WF2/WF7 prioritization.
Right now nothing feeds what actually converted back into the scoring model, so
the ICP weights and keyword tiers can only ever encode a prior belief, never a
learned one.

**Live chat only; propose-only.** It rewrites the scoring model (shared skill
state), so a human signs off every delta. Writes go **only** through the
single-source path in step 4. `references/funding-sources.md`,
`references/style-and-examples.md`, and `scripts/scoring_taxonomy.json` are all
in play.

1. **Assemble the outcome set — both directions** (the cross-validate
   principle; a model tuned on wins alone overfits):
   - **Wins / advanced:** All Accounts at Client (2) / Active (4) / Partner (9)
     / Complete (3); Won funding items; and the converted deals documented in
     `style-and-examples.md` Patterns A–E (Recovered Potential, One Scientific,
     Capture6, OCOchem, GlycoSurf, Phinix).
   - **Losses / kills:** WF12 Dead (6) / Unqualified (11) **with their logged
     reasons** (that's why the reason is mandatory at kill time). Treat Bounced
     (8) as contact-data noise, not a fit signal — exclude it.
   Pull each with its capability tags, industry, HQ, and funding hook.
   **Declare coverage honestly:** JE's absolute win count is modest, so this is
   **directional, not statistical** — say so, and never overfit to two or three
   deals.
2. **Look for signal, both directions:**
   - Which **capability tags** are over-represented in wins vs kills? Is any
     bullseye tag quietly predicting *kills* (a sign it's mis-tiered)?
   - Which **industries / funding hooks** convert — does a live non-dilutive
     deadline actually correlate with wins (the thesis behind the Compelling
     Event 2.0 weight)?
   - Which **keyword-tier terms** actually appeared in winners' descriptions —
     is a tier-3 term behaving like a tier-4, or vice versa?
   - Do the current default weights (Compelling Event 2.0, Access to Economic
     Buyer 1.5) hold up against the outcomes, or should they move?
3. **Propose calibration deltas — each with its evidence and the exact edit:**
   an ICP weight change (`icp_weights`), a keyword promotion/demotion between
   tiers, or a bullseye/adjacent tag to add because winners kept showing it.
   Every proposal **names the win/kill examples behind it** — no change without
   evidence, and no change justified by a single deal.
4. **Apply on Riley's go — only via the single-source path.** Edit
   `scripts/scoring_taxonomy.json` **first** (it is canonical), then mirror the
   same change into the human tables in `references/funding-sources.md` (per
   its "Canonical source" banner), and re-confirm the two match. Never edit one
   without the other — keeping them in sync is the whole point of the taxonomy
   split. A WF5 rebuild then re-scores the book on the new model.
5. **Digest:** deltas proposed (with the evidence deals), what Riley approved,
   which taxonomy files were touched, and a reminder to run WF5 (rebuild the
   workbook) so the new weights propagate to the ranking.
