# Workflow 12 — Disqualify / kill + book hygiene

Trigger: "kill {account}", "disqualify {account}", "mark {account} dead",
"these are dead", "book hygiene", "prune dead suspects", "clean up my book";
also the landing spot for Workflow 10's "contact or drop → **drop**" and
"push or park → **park/kill**" branches, and for a confirmed-negative reply the
outreach skills surface.

**Live chat only; propose, then write on the operator's go.** A kill is a
judgment call and a write to the shared CRM — never scheduled, never auto (see
SKILL ground rules and the Cadence note; kill decisions stay in live chat).
**Only your own accounts** (Owner == `MY_USER_ID`): another owner's
dead-looking card is intel for that owner, never your write.
`references/monday-ids.md` is required (Status label map + kill recipe).

The mechanism: All Accounts Status has three terminal labels that sit **outside**
the book-pull filter `[0,14,103]` — `Dead` (6), `Unqualified` (11), `Bounced
(SPAMED)` (8). Moving a card to one of them drops it from every book pull
(WF2 batching, WF6 deadlines, WF10 pulse) automatically, so dead accounts stop
resurfacing without any per-workflow skip list. WF7 (whole-CRM name dedupe)
still sees it — by design, so it can't be re-added — and echoes it as
"disqualified," not as a live near-miss.

## Mode A — targeted kill (operator named the accounts)

1. **Resolve + confirm ownership.** For each named account, `contains_text`
   search All Accounts (`7253021439`); confirm `Owner == MY_USER_ID`. If a
   teammate owns it, **stop** — surface it as intel for that owner, don't
   write. Confirm it's the right company before killing (cf. the Safire
   *Insurance* vs defense-battery Safire flag — a namesake is not your target).
2. **Pick the terminal status that fits the reason** (never guess — the label
   carries meaning downstream):
   - **Unqualified (11)** — fails ICP / not a fit: pure-software with no
     hardware to build around, wrong sector, out-of-scope size. The fit-miss
     kill (matches the `seq1-fit-filter-inclusive` memory).
   - **Dead (6)** — was a real prospect but the deal/relationship is over:
     explicit no, chose a competitor, folded, or a confirmed kill (the WindTP
     case in the outreach example bank).
   - **Bounced (SPAMED) (8)** — reserve for contact-data dead-ends (email
     bounced / spam-flagged), not a fit judgment.
   - **Do NOT use Cold (7) here.** Cold = gone quiet but re-warmable — that's
     WF10's Cooling bucket, a different state. If the account is merely quiet,
     route it back to WF10, don't kill it.
3. **Record status + reason on the operator's go.** Set Status to the chosen
   label AND log an update/comment: `Disqualified {date} by {operator}:
   {status} — {reason}` (kill recipe in `references/monday-ids.md`). **The
   reason is mandatory** — a bare status change with no reason gets
   re-litigated next quarter and wastes the next prospecting run. Never delete
   the card (ground rules: only the operator deletes their own data).
4. Digest the result (Mode-A digest below).

## Mode B — hygiene sweep (find kill/park candidates)

5. Pull your book (your-book recipe, `references/monday-ids.md`). Flag — do not
   auto-kill — candidates, each with its evidence:
   - **Aging Suspects, ~zero interaction** (cross-ref WF10 first-touch-overdue):
     contact-or-drop. A Suspect that never got a first touch and no longer
     fits is an Unqualified; one that fit but went nowhere is a judgment call
     for the operator.
   - **Long-stalled in stage, no movement** (cross-ref WF10 stalled): push or
     park — parking a truly dead one is a Dead.
   - **Bounced / undeliverable contact data** (cross-ref the standing
     data-quality flags): Bounced (SPAMED), or a data-quality flag if the
     account itself is still real.
   - **Confirmed wrong-company cards** (e.g. Safire Insurance): these are data
     errors, **not** kills — flag for the operator to fix/relink, don't
     disqualify the real underlying account.
6. Present the candidate list — account, evidence, suggested terminal status —
   and let the operator confirm which to kill. Write only the confirmed ones
   via step 3. Everything else stays open.

## Digest

- **Killed:** account → status (Dead / Unqualified / Bounced) → reason, per line.
- **Parked / at-risk, still open:** the candidates the operator kept.
- **Data flags, not kills:** wrong-company / mis-linked cards to fix.
- Reminder: killed cards now drop from WF2 / WF6 / WF10 book pulls
  automatically, and WF7 dedupe will echo them as "disqualified {date}:
  {reason}" if they resurface on a prospect list — so the reason you logged in
  step 3 is what stops the re-litigation.
