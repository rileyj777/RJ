---
name: funding-opportunities-pipeline
description: Johnston Engineering (JE) BD playbook — funding pipeline, CRM, and Miller-Heiman Strategic Selling on monday.com. Use whenever asked to refresh the Funding Opportunity Pipeline board, batch/pull/rank accounts, score the book, map contacts or buying influences, tag Economic/Technical/User buyers, run gap analysis on a prospect or conference list, rebuild the Strategic Selling workbook, build a grant-pursuit brief or one-pager for an account + solicitation, run the weekly 2-min status, relationship pulse, or pipeline brief, find new suspects, hunt for net-new funding offices or programs, scout National Lab IP for JE commercialization fit, or mentions SBIR/STTR, DARPA, ARPA-E, DoD waves, blue sheets, ICP scoring, tech transfer, CRADA, or grant deadlines — even short voice fragments like "refresh the funding board", "batch more", "find new suspects", or "scout lab IP".
---

# JE Strategic Selling & Funding Pipeline

_v4.2 (multi-operator) — the 10 workflows of v3.3 restructured for
progressive disclosure (v4.0: this body is the router; procedures live in
`references/wf-*.md` and load only when their workflow runs), plus
Workflow 11 (grant-pursuit brief, `wf-grant-pursuit.md`, v4.1). v4.2 is a
quality-hardening pass across all 11 workflows: idempotent reads-before-writes
on the shared CRM, coverage-honesty carried into the emitted digests,
compliance defense-in-depth at every send/export escape hatch, deterministic
matching/scoring, and internal spec-vs-spec contradictions reconciled.
v4.2.1: clarified the re-bucket rule so dated items in the thematic Lab-tech /
State groups stay in their group and are surfaced in the digest rather than
moved to a date bucket. v4.2.2: tuned the ICP scoring model — non-flat default
criteria weights (Compelling Event 2.0, Access to Economic Buyer 1.5, rest
1.0, all operator-editable) and a tiered Industry-Fit pre-score where bullseye
FOAK tags count double, so a lone sweet-spot tag outranks a lone adjacent one.
v4.2.3: rebuilt the `funding-sources.md` Source directory into a structured,
URL-bearing, agency-grouped list of government data sites (all verified
2026-07-24) — cross-agency master portals (SBIR.gov, Grants.gov,
SAM.gov/FPDS, USAspending.gov, FedConnect) plus DoD/DoW, DOE, and every
federal grant/SBIR sub-agency in a JE lane; also added the SBIR.gov award DB
and USAspending.gov as structured Workflow-7 suspect sources.
v4.3: (1) rebuilt Workflow 5's `build_workbook.py` into a data-free scaffold —
account/contact/angle/gap data now come from live-pulled JSON, counts and the
zero-contact / no-economic-buyer red-flag lists are computed at build time, and
the scoring taxonomy (keyword tiers, junk filter, capability tags, ICP weights)
moved to one canonical `scripts/scoring_taxonomy.json` the builder reads,
ending its silent duplication with `funding-sources.md`; no frozen snapshot
blocks and no hardcoded upload filenames remain. (2) Added a `wf9-lab-rotation`
memory so National-Lab IP scouting rotates labs/lanes like WF7 does. (3)
Reworked Workflow 10 around JE's actual stack — a monday-native last-touch
signal (item update log + status history) plus HeyReach — after confirming JE
runs no Salesflare or other connected sales-activity CRM; proposal stage is
operator-supplied or unknown, never fabricated. (4) Added Workflow 12
(disqualify/kill + book hygiene, `wf-hygiene.md`) and documented the full All
Accounts Status label map in `monday-ids.md` — killing moves a card to a
terminal status (Dead/Unqualified/Bounced) outside the book filter, so it drops
from WF2/WF6/WF10 automatically and WF7 dedupe echoes it as disqualified.
(5) Added Workflow 13 (proposal-kickoff handoff, `wf-proposal-kickoff.md`) —
the bridge from a won WF11 pursuit to a scoped JE proposal skeleton; it defers
to the root `CLAUDE.md` for the proposal standards and never prices (Riley owns
pricing). (6) Added Workflow 14 (win/loss calibration, `wf-calibration.md`) — a
periodic pass that feeds won/killed outcomes back into the ICP weights and
keyword tiers, writing only through the canonical `scoring_taxonomy.json` →
`funding-sources.md` sync path._

Operating playbook for a sales engineer in Business Development at Johnston
Engineering (JE). JE's mission: "Propel the commercialization of
first-of-a-kind technologies through advanced engineering design, analysis,
build and test." Clients are cleantech / energy / critical-materials / defense
hardware startups. JE sells DFM, custom machinery, thermal/CFD and structural
analysis, electrolyzers, energy storage builds, test fixtures, containerized
systems, and pilot plants — so *non-dilutive funding deadlines are the
compelling events* that open JE deals.

Operator messages are often voice-dictated: expect typos and fragments.
"Refresh the funding board" and "batch more" are standing triggers, not new
requests to clarify.

Three layers: **monday.com boards** (live state — the Funding Opportunity
Pipeline holds deadlines; the CRM holds the book and the buying-influence
map), the **Strategic Selling workbook** (Excel scoring model, rebuilt on
demand by `scripts/build_workbook.py`), and **this skill** (the playbook that
makes every run identical).

## Step 0 — Identify the operator (before any board read/write)

This skill is shared across JE BD (Riley, Parker, David, Austin, Shane, …):
one shared CRM (All Accounts / All Contacts), one funding board *per
operator*. Before the first read or write in any workflow, call monday
`get_user_context` once and capture:

- `MY_USER_ID` — the operator's monday user id
- `MY_EMAIL` — sanity-check it's a johnstonpe.com account
- `MY_FUNDING_BOARD` — from the per-operator table in
  `references/monday-ids.md` (keyed by `MY_USER_ID`; fallback rule is there)

Substitute these wherever recipes show them; never hardcode a person's id or
a single funding board. Scheduled runs, auto-add pre-authorizations, and
memory are all per-operator; only `MY_USER_ID` and `MY_FUNDING_BOARD` vary —
schema, scoring, and sources are shared.

## Ground rules (apply to every workflow)

- **Only touch your own accounts.** Create or modify only accounts you own
  (Owner == `MY_USER_ID`). Every other account, whoever owns it, is
  **intel-only**: surface it to that owner and never solicit, re-tag, re-own,
  or otherwise modify it. On a shared CRM this rule never bends.
- **Verify before you write.** Never put a deadline on the board from memory —
  web-search the solicitation first. Government dates slip; DoW/DARPA SBIR
  topics close at **12:00 PM ET (noon)**, not midnight. Cite what you found in
  the item's Notes with "VERIFIED {date}: {source}", where {date} is the day
  you checked the source.
- **Flag, don't delete.** Wrong-company contacts, suspect emails, bad
  enrichment: mark them (⚠ note, pink flag) and tell the operator. Only the
  operator deletes their own CRM data.
- **Never auto-assign a Coach.** Per Miller-Heiman, a Coach must meet all
  three criteria (you have credibility with them; they have credibility with
  the buying influences; they want JE's solution). Titles can suggest
  Economic/Technical/User buyers; a Coach is earned — the operator sets it.
- **Re-bucket by close date on every touch.** Deadline groups: <2 weeks,
  2–6 weeks, 6 weeks–3 months, Watchlist. Exception: dated items that live in
  the thematic groups (🧪 Lab tech, 🏛️ State programs) stay in their group and
  get surfaced in the deadline digest rather than moved to a date bucket, so
  their thematic grouping is preserved (e.g. INL BA-1678 closing inside 2 weeks
  stays in Lab tech and is still called out under <2-week deadlines).
- **End every workflow with a short digest** (5–8 lines): what changed, what's
  due inside 2 weeks, what still carries a "verify" flag, and what the run
  didn't cover.

## Quality bar (every workflow)

- **Every fact carries a date and a source.** A deadline, award, or title
  without "VERIFIED {date}: {source}" is a claim, not a fact — say which it is.
  Prefer the primary source (the solicitation page, the SEC filing, the lab's
  own portal) over news coverage; when only secondary coverage exists, say so.
- **Declare coverage honestly.** Every run states what it did NOT cover —
  lanes unscanned, portals unreachable, pages truncated, systems that failed
  to connect. A digest that implies full coverage when three portals were
  JS-blocked is worse than a smaller honest one.
- **Cross-validate both directions.** When two sources of truth exist (the
  board vs the reference deadline snapshot, monday vs HeyReach), check both
  ways: items in one and missing from the other are findings, not noise.
- **Every recommendation lands somewhere.** A shortlisted tech, opportunity,
  or suspect names the specific account, solicitation, or teammate it maps
  to and the one next action — "interesting" without a landing spot gets cut.
- **Surface the second-order deadline.** Q&A cutoffs, LOI gates, abstract
  prerequisites, and bucket-crossing dates are where deals die quietly; hunt
  for them, don't just relay the headline close date.

## Workflow router — read the file, then run the numbered steps

| # | Workflow | Triggers | Read first |
|---|---|---|---|
| 1 | Funding board refresh | "refresh the funding board" | `wf-funding.md` + `funding-sources.md` |
| 8 | Net-new funding-source discovery | "find new funding sources/offices", "what aren't we tracking" | `wf-funding.md` + `funding-sources.md` |
| 10 | Monday relationship pulse | "relationship pulse", "who needs a touch", "2-min lead update" | `wf-monday-cadence.md` |
| 6 | Monday 2-min deadline brief | "2-min status", "pipeline brief", "Monday brief" | `wf-monday-cadence.md` |
| 7 | New-suspect search | "find new suspects", "prospect", "fill the pipeline" | `wf-monday-cadence.md` + `funding-sources.md` |
| 2 | Account batching & ranking | "batch more", "pull/rank accounts" | `wf-accounts.md` |
| 3 | Contact mapping (buying influences) | "map contacts", "tag buying influences" | `wf-accounts.md` |
| 4 | Gap analysis on a prospect list | uploaded conference/attendee list, "check this list" | `wf-accounts.md` + `funding-sources.md` |
| 5 | Rebuild Strategic Selling workbook | "rebuild the workbook", "update the scorecard" | `wf-accounts.md` |
| 9 | National Lab IP scouting | "scout lab IP", "tech-transfer scan" | `wf-lab-ip.md` + `funding-sources.md` |
| 11 | Grant-pursuit brief | "pursuit brief", "one-pager for {account} on {solicitation}", "how do we play X with Y" | `wf-grant-pursuit.md` + `funding-sources.md` |
| 12 | Disqualify / kill + book hygiene | "kill/disqualify {account}", "mark dead", "book hygiene", "prune dead suspects", "clean up my book" | `wf-hygiene.md` |
| 13 | Proposal-kickoff handoff | "proposal kickoff for {account}", "scope a proposal", "won {account} — start the proposal", "turn this pursuit into a proposal" | `wf-proposal-kickoff.md` (defers to root `CLAUDE.md`) |
| 14 | Win/loss calibration | "calibrate the model", "win/loss review", "tune ICP from outcomes", "what's converting" | `wf-calibration.md` |

All workflow files are in `references/`. Also read, when relevant:

- `references/monday-ids.md` — **before any monday read/write**: board /
  column / group IDs, per-operator funding boards, filter recipes, API
  landmines.
- `references/funding-sources.md` — deadlines, verify flags, source
  directory, keyword tiers + junk filter, lab-IP rubric, digest template.
- `references/style-and-examples.md` — **only** when drafting outreach copy
  directly (Workflow 10 step 7, Workflow 11 cover note): JE house voice,
  bottleneck-to-capability method, exemplars. Synced copy from the
  `je-outreach-seq1` skill — if that copy is edited, re-copy it here so the
  two don't drift.

Workflows hand off to each other (8→1, 10→6→7, 2→5, 4→7, 10→12 whenever a
drop/park decision needs recording, 7↔12 so dedupe echoes disqualified cards,
1/6/9→11 whenever a deadline lines up with an account, 11→13 when a pursuit
converts to a proposal, and won/killed outcomes from 11/12 feed 14): when a
handoff crosses files, read the target file at that point.

## Cadence

Friday: Workflow 1. Monday: Workflow 10 (relationship pulse), then Workflow 6
(deadline brief), then Workflow 7 (new-suspect search) — the whole Monday
cadence lives in `wf-monday-cadence.md`. Monthly: Workflow 8 (net-new
sources), then Workflow 9 (lab IP, rotating lanes), plus Workflow 2 (+5 as
needed). Quarterly: Workflow 14 (win/loss calibration). Workflows 4, 11, 12,
and 13 are on-demand; 11, 12, 13, and 14 are **live chat only** — they produce
outbound-facing material (11, 13) or write shared state (12 disqualifications,
14 the scoring model), so none is ever scheduled.

In Cowork, each can be a scheduled task (`/schedule`); scheduled runs can't
pause to ask questions, so keep judgment calls (Coach tags, kill decisions,
deleting data, adding Suspects or creating board items unless pre-authorized)
in live chat. Workflow 8 may add net-new sources to
`references/funding-sources.md` automatically; Workflows 9 and 10 propose and
never write to the CRM on their own.
