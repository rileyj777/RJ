# Workflows 2, 3, 4, 5 — accounts, contacts, gap analysis, workbook

CRM-side workflows. `references/monday-ids.md` is required for 2 and 3;
Workflow 4 needs the junk filter + keyword tiers in
`references/funding-sources.md`; Workflow 5 (workbook) feeds on fresh pulls
from 2 and 3.

## Workflow 2 — Account batching & ranking

Trigger: "batch more", "pull more accounts", "rank accounts".

1. Pull the next page of your accounts from All Accounts using the owner +
   status filter recipe in `references/monday-ids.md`. Use slim columns
   (status, industry, fit tags, location). Cursors expire (~60 min) — if the
   cursor errors, re-run the filtered query from page 1 and skip already-seen
   pages.
2. Cluster the pulled accounts by their capability-fit-tag values
   (dropdown_mm1h5y5v — e.g. battery, hydrogen/electrolyzer, thermal,
   critical minerals, mining machinery, space/defense; examples, not a
   closed taxonomy, so cluster on whatever tags are present) and append them
   to the matching funding items' Related accounts on `MY_FUNDING_BOARD`.
   That column overwrites (monday-ids landmine 4), so write old+new and skip
   names already in the string — a page-1 restart (step 1's fallback) or a
   repeated "batch more" must not double-list an account. Surface any account
   with no capability tag as incomplete data — it can't cluster or earn an
   Industry Fit pre-score.
3. Note state-program matches (account HQ state → state item on
   `MY_FUNDING_BOARD`).
4. If a re-rank is wanted, run Workflow 5 (workbook rebuild) with the fresh
   data.

## Workflow 3 — Contact mapping (buying influences)

Trigger: "map contacts", "tag buying influences", or after new contacts land.

1. Pull contacts for target accounts: filter All Contacts on `contact_account`
   `any_of` [account item IDs]. **Mirror columns (Account Owner) are NOT
   API-filterable** — always filter through the account-link column.
2. Suggest roles from titles: CEO / President / CFO / COO / Co-Founder →
   Economic Buyer (releases the money, final approval). CTO / Chief Engineer /
   VP-or-Sr-Dir of R&D → Technical Buyer (screens on specs, can say no but not
   yes). VPs/Directors/Managers of Manufacturing, Operations, Engineering
   Implementation, Products → User Buyer (lives with JE's work) — a VP of
   Manufacturing/Operations is a User Buyer, not the R&D Technical Buyer above.
   Sales / PR /
   Legal / HR → leave blank. Coach → never auto-assign (see ground rules).
   Titles with no clean functional signal (a bare "Director" or "Founder",
   business-development/commercial roles, dual-hat startup titles) also leave
   the tag blank, noted for the operator — a mis-tagged buyer silently
   corrupts the workbook, Blue Sheet, and gap analysis downstream, so a
   missing tag beats a guessed one.
3. Write tags to the Buying Influence dropdown with one **batched
   `all_api_write` mutation** (alias one `change_multiple_column_values` per
   contact, `create_labels_if_missing: false`, short JSON variables — see the
   API landmines section of `references/monday-ids.md`). Keep
   `create_labels_if_missing` **false** — the three role labels are already
   seeded, so any label creation here would be a typo'd junk label on a
   shared board (same reason the new-suspect recipe keeps it false). Write
   only to contacts whose Buying Influence is currently blank — the step-1
   pull already returns `dropdown_mm525a5g`, so use it. A `{labels}` write
   replaces the dropdown (landmine 5), so re-tagging would silently overwrite
   an operator-set Coach or a prior role; skipping already-tagged contacts
   also makes re-runs idempotent.
4. Data-quality pass: email domain must match the company; flag mismatches
   (e.g., an insurance-company domain on a defense-battery account) and any
   account with **zero contacts** — those are uncovered bases, a red flag in
   Miller-Heiman terms. Also flag accounts that have contacts but no Economic
   Buyer among them — no known line to the money is the sharper Miller-Heiman
   uncovered base than the zero-contact check.

## Workflow 4 — Gap analysis on a prospect list

Trigger: the operator uploads a conference/attendee/coalition list, or says
"check this list for ones I'm missing".

1. Extract company names + any description/category columns.
2. Normalize names (lowercase; strip punctuation, parentheticals, and suffixes
   like Inc/LLC/Corp/Technologies/Systems/Energy).
3. Drop junk via the filter regex in `references/funding-sources.md`
   (associations, media, job boards, universities, advisors, funds…).
4. Dedupe against the whole shared CRM (all owners), not just your own
   accounts. A list company already owned by a teammate isn't a gap — per the
   ground rules it's intel for that owner, never your Suspect. Don't drop
   prefix/fuzzy matches silently — that's where distinct companies collapse
   after suffix-stripping (e.g. "Solid Energy" folded into "Solid Power").
   List the borderline (prefix/fuzzy) drops with the CRM name each matched so
   the operator can eyeball them; a real prospect suppressed as a false dupe
   defeats the workflow. Exact-name dupes needn't be itemized.
5. Score survivors with the keyword tiers (5/4/3) in the reference file;
   include score ≥ 3. Pre-qualified lists (a "Verdict = QUALIFIED" column)
   force-include at ≥ 4.
6. Companies on **2+ lists get a ★ and priority** ("add as Suspect"). Lead
   the output with a coverage line — "rows found N → junk-dropped J → deduped
   D → included (≥3) K" — and flag any rows, sheets, or columns you couldn't
   parse (lists arrive as PDFs/screenshots/multi-sheet books). Then give a
   sorted table (or workbook Gap tab) with source lists, evidence snippet,
   and suggested next step; show the numeric score/tier per row and make the
   evidence snippet the verbatim triggering text plus the keyword matched, so
   each row is auditable against the source rather than a paraphrase
   indistinguishable from an invention.

## Workflow 5 — Rebuild the Strategic Selling workbook

Trigger: "rebuild the workbook", "update the scorecard", or after a big batch.

1. `scripts/build_workbook.py` builds the whole workbook (READ ME, Account
   Scorecard with live weighted ICP formulas, Buying Influences map, Blue
   Sheet, Gap Analysis). **The account/contact data blocks inside it are
   example data from a prior rebuild** — before rebuilding, refresh the `b2`/`b3`
   account lists and the `contacts` list from fresh monday pulls (Workflows
   2–3), and replace the transcript-parsing block with typed data if the
   original transcript is unavailable. Those aren't the only frozen blocks in
   the script: the funding-angle map, the zero-contact RED FLAGS list, and
   the READ ME headline counts (180 accounts / 84 contacts / 21 pre-tagged)
   are all July-12 snapshots too. Refresh the angle map from the current
   pipeline board and compute the counts and red-flag list from the refreshed
   data at build time — otherwise the finished workbook shows a stale angle
   as a board-sourced fact and its READ ME contradicts its own sheets. The
   angle-to-account match is a loose substring, so also confirm each angle
   landed on the right account. Most rebuilds ("update the scorecard", "after
   a big batch") have no conference lists to gap-analyze, yet the Gap Analysis
   block reads fixed upload filenames without guards — one missing file
   crashes the whole build before any tab is written. Guard those reads or
   skip the Gap tab when no lists were uploaded, and gap-analyze only the
   lists actually provided this session.
2. The scoring model (keep exactly): five ICP criteria from the JE training —
   Industry Fit, Company Size Fit, Compelling Event Present, Access to
   Economic Buyer, Growth/Follow-On Work Potential — each 0–5, adjustable
   weights in row 2, `SUMPRODUCT`-weighted %, `RANK`, A–D tier
   (≥75/55/35%), `COUNTBLANK` completeness. Industry Fit is pre-scored from
   CRM capability tags; the other four are the operator's judgment (yellow cells).
3. **Mandatory:** run `python /mnt/skills/public/xlsx/scripts/recalc.py
   <file>` and ship only on `"status": "success"` with zero errors. Spot-check
   2–3 computed cells against hand math before delivering.
4. Deliver to outputs and close with the standard digest — and be honest
   about the ranking's state: a fresh build has only Industry Fit prefilled,
   so every account sits at tier D and the ranks are provisional until the
   operator scores the other four criteria. Present it as a scaffold awaiting
   judgment, not a finished book.
