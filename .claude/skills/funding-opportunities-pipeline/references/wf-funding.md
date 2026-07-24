# Workflows 1 & 8 — Funding board refresh + net-new source discovery

Both need `references/funding-sources.md` open (Workflow 1 works its
verify-flags list; Workflow 8 edits its Source directory) and
`references/monday-ids.md` for board writes.

## Workflow 1 — Funding board refresh

Trigger: "refresh the funding board" (any phrasing). All reads and writes
target `MY_FUNDING_BOARD` (Step 0) — the operator's own funding board.

1. Open `references/funding-sources.md`; work the **verify-flags list** first —
   each is one targeted web search. Update Notes, dates, and group placement.
   Then, independent of the flag list, re-verify every board item closing
   within 2 weeks against its primary source — a hand-curated flag list can't
   be trusted to always include them, and near-term dates are the costliest to
   get wrong (a slipped date, or a noon close read as midnight).
2. Scan for **new** opportunities: DoD/DARPA SBIR topic pages, ARPA-E eXCHANGE,
   NSF/DOE/NIH/USDA SBIR calendars, and the state programs relevant to
   accounts in the book; plus any other source in the directory not already
   named here, so vehicles WF8 added actually get swept. Add new items with
   Source, Mechanism, Solicitation #, Closes, Fit, Link, Notes, and Related
   accounts filled.
3. Re-bucket everything by close date — except dated items in the thematic
   groups (🧪 Lab tech, 🏛️ State programs), which stay in their group and are
   surfaced in the deadline digest rather than moved to a date bucket. Dedupe against existing items before
   creating (search the board by solicitation number first; for the many
   opportunities with no number yet — waves, standard due dates, prizes —
   match on source + mechanism + close date instead, so step 2 doesn't
   re-mint them every refresh).
4. **Two-way cross-check** (catches silent drift): (a) every entry in the
   reference deadline snapshot should have a live board item — a snapshot
   entry with no item is a missing add (or gets an explicit "n/a — {reason}"
   note); (b) every board item whose deadline has passed gets proposed
   Stage=Passed with a rename, so dead items never look live; (c) the dated
   deadlines you added in step 2 (and Workflow-8 handoffs) get written into
   the snapshot too, with their VERIFIED date — otherwise the baseline only
   shrinks and the newest, most time-sensitive items never get cross-checked.
   Keep it to live dated deadlines, not a full board mirror; passed rows still
   archive out, so it stays bounded. After the refresh, update the snapshot's
   "verified {date}" header in `references/funding-sources.md` so the next run
   knows its baseline, and move passed snapshot rows to an "Archive (passed)"
   section at the bottom
   of that file — the live table stays only as long as the live deadlines.
5. Match new/updated opportunities to accounts using the "Account clusters →
   opportunity mapping" table as the key; the Related accounts column
   overwrites, so read its current value, dedupe, then write old + new.
6. Digest: verified items, new items, moved items, cross-check findings
   (missing adds, passed items), next hard deadlines + any second-order
   cutoffs (Q&A windows, LOI gates), remaining verify flags.

## Workflow 8 — Net-new funding-source discovery

Trigger: "find new funding sources/offices/programs", "what offices are we not
tracking", "sweep for new vehicles"; also part of the monthly cadence.

Workflow 1 scans *known* sources for new opportunities. Workflow 8 finds the
*sources themselves* — offices, programs, and vehicles not yet in the Source
directory — and adds the qualifying ones back into
`references/funding-sources.md` so Workflow 1 starts covering them.

1. Load the "Source directory" in `references/funding-sources.md`. Anything
   already there is not "new." (The hunting grounds to sweep are listed in
   step 2 below.)
2. Sweep the hunting grounds — 2–4 targeted searches, rotating the lanes. The
   major federal vehicles (SBIR.gov, Grants.gov, SAM.gov, FedConnect, the
   DoD/DoW innovation orgs, DOE offices, and the SBIR sub-agencies) are now
   tracked in the Source directory, so hunt the layer they don't cover:
   newly created or renamed offices and programs (use the MITRE AiDA map,
   aida.mitre.org, to spot DoD offices not yet in the directory); component /
   service SBIR offices and new DARPA/ARPA-E program launches not individually
   listed; new state/regional funds and EDA Tech Hubs in JE's account states;
   and private/foundation/corporate vehicles, which stay thin in the directory
   (prize sponsors, corporate lab/venture programs, prime supplier-innovation
   programs). A source already in the directory is a Workflow-1 scan target,
   not a WF8 find.
3. Qualify before adding: the source must fund hardware or first-of-a-kind
   equipment in a JE lane, and a JE account (or JE itself) must be able to be
   an applicant or sub. Drop software-only, university-research-only, and
   dilutive-only vehicles.
4. Web-verify each net-new qualifying source is real and active — i.e., it
   has run a solicitation in the last ~24 months or posts a forward cadence,
   confirmed on the program's own funding page rather than announcement
   coverage; a source only announced, never funded, gets a next-open note,
   not an active add — then add it to the Source directory in
   `references/funding-sources.md` with a one-line
   what-it-funds / who-can-apply / cadence note and URL. This is a
   reference-file edit, not a board write.
5. Hand off: for any new source with an open solicitation now, run Workflow 1
   steps 2–4 on it (pull the item onto `MY_FUNDING_BOARD`, verify the close
   date, map accounts). Sources with nothing open yet get a next-open note in
   their directory entry — not a board item; WF8 only edits the reference
   file.
6. Digest: sources added (name + what they fund), any that produced an
   immediate board item, next expected open dates.
