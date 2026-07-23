# Workflows 10, 6, 7 — the Monday cadence (run back to back)

Order: Workflow 10 (relationship pulse) → Workflow 6 (deadline brief) →
Workflow 7 (new-suspect search). Each also fires standalone on its own
triggers. `references/monday-ids.md` is required throughout; Workflow 7 also
needs the prospecting sources + keyword tiers in
`references/funding-sources.md`.

## Workflow 10 — Monday relationship pulse (2-minute lead/account brief)

Trigger: "relationship pulse", "who needs a touch", "2-min lead update",
"Monday accounts brief"; first step of the Monday cadence.

The engagement counterpart to Workflow 6: it surfaces the highest-priority
Suspects / Prospects / Leads by *relationship state* (recency of contact, how
long they've been in play, whether a proposal is out), not by funding
deadline. Your own book only (Owner == `MY_USER_ID`); read-only / propose-only.

The three signals do not live on monday — the CRM board holds only who/stage/
owner. Sources: **monday** (`7253021439`) = the book, stage label, and
ownership scope; **Salesflare** = interaction recency (R), opportunity /
proposal stage + date (P), and time-in-stage; **HeyReach** = LinkedIn touch +
reply recency for outreach-stage leads not yet in Salesflare. Resolve the
Salesflare/HeyReach tools via `tool_search` on first run. If either system
is unreachable, say so in the brief's first line and state which signals are
therefore missing — a pulse built from monday alone must never read as if it
had checked engagement data.

1. Scope the book: pull your accounts from monday with the your-book recipe in
   `references/monday-ids.md` (Owner `any_of [person-<MY_USER_ID>]`, Status
   `any_of [0,14,103]`). This is the authoritative "yours" list plus each
   account's stage.
2. Pull engagement where the action is (not the whole book): from Salesflare,
   your accounts/opportunities with recent activity, an open opportunity, or a
   quiet/stalled timeline — capture R (last interaction), P (proposal/quote
   stage + date), and days-in-stage. From HeyReach, your active campaigns'
   leads with last message sent / reply received / no-reply — R for
   outreach-stage suspects. Relationship age (D) = Salesflare opportunity or
   account age, or the monday item's created-date + status-change history as a
   fallback.
3. Match to the book by company name (the book pull returns names, not a
   domain column) for Salesflare↔monday and contact name/LinkedIn for
   HeyReach↔monday; treat near-identical names as tentative, since a
   look-alike ("Elements" vs "Infinite Elements", cf. landmine 9) binds a
   signal to the wrong card — the core trust failure of this brief. Flag
   unmatched signals, never guess. Treat absence with care: the step-2 pull
   is scoped, so an account it didn't return isn't proven uncontacted — it
   may be a gone-quiet Cooling target; confirm its last-touch date before
   calling it First-touch/zero-interaction (and before dropping it from the
   brief).
4. Bucket each account by the single highest-priority trigger it hits (standard
   clock — proposal follow-up at 5–7 days, cooling at 14 days):
   - **Proposal pending** — proposal/quote sent, no decision, ≥5–7 days quiet → follow up (top; money on the table).
   - **Warm, owe a next step** — inbound reply/meeting in the last few days, thread still open → advance now.
   - **Cooling** — was engaged, ≥14 days silent, no proposal yet → re-warm before it dies.
   - **Stalled in stage** — long time-in-stage, no recent movement → decide: push or park.
   - **First-touch overdue** — aging Suspect, ~zero interactions across both systems → contact or drop (an uncovered base, a Miller-Heiman red flag).
5. Rank by urgency (Proposal pending → Warm → Cooling → Stalled → First-touch);
   tie-break by days waiting, longest first. Cap ~5–7; lead with the ≤3 that
   need action today.
6. One line per item:
   `Account (stage) · trigger · last touch (Nd) · in play (Nd) · proposal? · one next action`
   (in play = D, relationship age from step 2).
   Open with a header that counts whichever buckets are populated, by their
   step-4 names (Proposal pending / Warm / Cooling / Stalled / First-touch) —
   so it can't understate the queue or use a label ("hot") that matches no
   bucket.
7. Propose the touches; write nothing to the CRM without the operator's go. On
   request, either hand the follow-up to the `je-outreach-seq1` skill, or draft
   it directly here: read `references/style-and-examples.md` first for the house
   voice and the bottleneck-to-capability method, and still run the
   `je-outreach-seq1` compliance gate before anything is sent (fission / HALEU /
   nuclear fuel-cycle = full hold, do not draft; defense / aerospace / ITAR =
   draft but hold for Andy; exec-tier contact = Andy owns the relationship). A
   draft is not a send. Otherwise use the message tools, or log a "surfaced
   {date}" note. Digest: today's action list, what's cooling, and any signals
   that wouldn't match across systems (a data-hygiene fix for the operator).

## Workflow 6 — Monday 2-minute status brief

Trigger: "2-min status", "pipeline brief", "Monday brief" (slide 38 of the JE
training deck — the agreed weekly cadence). This is the *deadline / deal* half
of the Monday cadence; Workflow 10 is the *relationship* half.

1. Pull funding items from `MY_FUNDING_BOARD` closing within 21 days + any
   item you're actively pursuing. The board has no Urgent flag, so use
   working state as the proxy — Stage = Reviewing/Pursuing/Submitted, or
   Fit = High — and say which signal you used. (Rows here are solicitations,
   not accounts.)
2. Hunt the **second-order deadlines** hiding inside and just past the
   window: TPOC Q&A cutoffs, LOI/abstract gates that decide who may even
   apply, and items just outside 21 days that need action now. Also list the
   next **bucket-crossing dates** ("item X crosses into <2 weeks on {date}")
   so nothing jumps buckets unnoticed between briefs.
3. Cross-check the reference deadline snapshot in
   `references/funding-sources.md` against the pulled items: a snapshot
   deadline inside the window with no board item is a gap — surface it.
   And compare dates on items that appear in both: a board Closes that
   disagrees with the snapshot date means one source is stale — the exact
   error this brief exists to catch, so flag it rather than silently
   trusting one.
4. List deadline-integrity red flags: unverified deadlines, passed deadlines
   still looking live, and blue sheets not updated in 14+ days (if blue-sheet
   freshness is unknowable from monday, say so and prompt for the workbook
   rebuild date). (Relationship-health flags — uncovered bases / zero-contact
   and cooling accounts — live in Workflow 10; don't duplicate them here.)
5. For each Best Few / Urgent deal, prompt the operator with the training's two
   questions: "How do I feel right now about closing this (-5…+5)?" and
   "What must change to reduce anxiety / assure success?" Attach one concrete
   de-risker per deal where you can see one (a question to file, a fact to
   confirm) — the question lands better with a next move attached.
6. Write any rating or note changes back to monday; end with the digest.

## Workflow 7 — Recurring new-suspect search

Trigger: closing step of every Monday brief; also fires on "find new
suspects", "prospect", "who's new", "fill the pipeline".

The profile: a company that just won non-dilutive money or closed a hardware
round has budget *and* a compelling event — exactly when a first-of-a-kind
technology needs JE's design/analysis/build/test help. Search where money was
just announced, not generic company lists.

1. **Drain the backlog first.** Open the latest Gap Analysis (workbook tab or
   last gap run) and take un-actioned ★ multi-list names before searching
   fresh — those already carry multi-source signal.
2. **Fresh prospecting** — 2–3 targeted web searches, rotating lanes weekly so
   thin clusters get covered (source list + rotation in
   `references/funding-sources.md`): new SBIR/STTR and ARPA-E selections,
   DoD/DARPA award announcements, American-Made prize semifinalists, state
   program awardees, accelerator cohorts, and fresh seed/Series-A hardware
   raises in JE lanes. "Rotating weekly" only rotates if a run remembers
   where the last one left off — otherwise it drifts back to the fat,
   familiar lanes (batteries, defense) and thin clusters stay unscanned.
   Before picking this run's 2–3 lanes, read the previous run's "lanes to
   hit next" from your per-operator memory (or the last digest); record the
   lanes covered and the next ones at the end.
3. **Qualify** with the keyword tiers + junk filter (score ≥ 4 unless the
   lane is thin; hardware-build evidence beats software every time).
4. **Dedupe via per-finalist name search** — run a monday name
   `contains_text` filter query on All Accounts for each finalist, against
   the *whole* CRM (~2,880), all owners (not `searchTerm` — its relevance
   match can hide exact hits behind fuzzy neighbors; see landmine 9 in
   `references/monday-ids.md`). Do **not** page through your book (or the CRM) to
   fuzzy-match first: your book is a subset of the CRM, so the per-finalist
   search already covers it, and a full book pull costs 20+ pages of API
   reads for nothing. Search name variants (short name, no suffix) to catch
   near-misses. Any hit already in the CRM is off the add list; if another
   rep owns it, it's intel-only for that owner (see ground rules), never
   poached.
5. **Route the near-misses — they are half the value of the run.** Any
   qualified candidate that turned out to already be in the CRM is
   fresh-money intel, not waste: if it's your account, name the hook and the
   advance move ("Accelsius raised a $24M Series A — worth advancing now");
   if a teammate owns it, put a one-line heads-up in the digest addressed to
   that owner (intel-only, never touch the card). Also report lane
   saturation honestly — "8 of 10 finalists were already tracked" is a
   signal to rotate lanes next run, and the digest should name which thin
   lanes to hit next.
6. **Shortlist ≤ 10 per run** in the digest:
   `Company | HQ | what they build | JE angle (capability + funding hook) | source`.
7. **Adding to CRM — propose by default.** Create Suspects only on the
   operator's go, using the new-suspect creation recipe in
   `references/monday-ids.md` (Status=Suspect, owner = `MY_USER_ID`, existing
   Industry/Fit tags only, provenance note). If the operator pre-authorizes
   auto-add for scheduled runs, cap at 5 per run and always stamp the source
   so entries stay auditable — it's a shared board.
