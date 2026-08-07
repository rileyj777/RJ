# Pre-send QA sweep — auditing stamped cards before Riley enrolls them

Read-only audit over cards that already carry a Disposition. Run it when Riley
asks to check the book before sending, or some variant of "is this batch ready
to go." Never drafts, never sends, never rewrites copy.

It exists because the drafting crawl cannot catch these: **any** Disposition
value drops a card out of the crawl, so a card that was stamped wrong is
invisible from that point on. The sweep is the only thing that looks back.

## The two failures that actually reach a prospect

1. **A gated draft whose `Hold` never landed.** The write partially applied,
   the draft overwrote its placeholder, and the card now sits at `Drafted` or
   empty with finished defense/ITAR or exec-tier copy in it. It reads as
   send-ready to a human scanning the board.
2. **A `Drafted` card with no linked contact.** Sends as "Hi ,".

Everything else the sweep finds is cosmetic by comparison.

## Procedure

Pull Riley's Suspects and Prospects with a **non-empty** Disposition
(`multiple_person_mm1hxs7c any_of ["person-95557556"]`,
`color_mm1hq3s1 any_of [0, 14]`, `color_mm5830h5 is_not_empty`), requesting
`text_mm1kyzgk`, `long_text_mm1ka0r6`, `long_text_mm1t32`, `color_mm5830h5`,
`account_contact`. Then check each card:

**Interlock checks (these are the point of the sweep):**
- `Drafted` **and** `account_contact` empty → not enrollable, would send "Hi ,".
- `Drafted` **and** fit-notes contain hold language (`HOLD`, `COMPLIANCE`,
  `Exec-tier`, `defense`, `ITAR`, `Andy`) → the Disposition contradicts its own
  notes. This is the silent-`Hold`-failure signature.
- Any Disposition **and** fit-notes carry a full-hold flag (fission, HALEU,
  radiological, nuclear fuel cycle, NQA-1) while the body holds finished copy →
  escalate immediately; that copy should never have been written.
- `Fit-miss` or `Park` **and** the body holds a finished email → decide which is
  right and say so; a real draft sitting under a kill-ish stamp is wasted work.
- Disposition empty **and** the body holds a finished email → an earlier run
  drafted but never stamped. Stamp it from the fit-notes.

**Content checks** (run `<skill-dir>/scripts/lint_draft.py` per card, by
absolute path, rather than reading for punctuation):
- em dash, greeting line, signature block, banned phrase, character count,
  Title Case subject, `\n\n` paragraph separation.
- Subject still the retired `Johnston Engineering - Mechanical Engineering
  Support for [Company]` format.
- Two cards sharing a subject line, or a body whose hook names a different
  company than the card. That is the batch-write cross-contamination signature
  from `board-mechanics.md`.

**Freshness checks:**
- Fit-notes hook older than ~6 months and the body opens with congratulations →
  the congratulations framing has expired and now reads as stale research.
- Fit-notes record a hook the notes themselves flag as unverified or
  fetch-blocked → fine to send, but say so in the report so Riley eyeballs it.

## Writes the sweep is allowed to make

Exactly one: correcting a Disposition that contradicts its own fit-notes, in
the safe direction only. A card whose notes say hold and whose stamp says
`Drafted` becomes `Hold`. **Never the reverse** — the sweep never promotes a
card to `Drafted`, because that is the value that makes copy sendable and it
belongs to a human. Name every correction in the summary.

## Report format

Group by severity, most dangerous first: send-blocking interlock failures,
then content failures, then freshness notes, then a clean count. For each,
name the card, the specific check that failed, and the one action that fixes
it. If nothing fails, say so plainly with the number of cards audited rather
than padding the report.
