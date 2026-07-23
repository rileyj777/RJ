---
name: je-outreach-seq1
description: Generate and write Johnston Engineering "Email Seq. 1" cold-outreach subjects and body copy onto the monday.com All Accounts board (7253021439) for Riley Jackson's Suspects and Prospects. Use whenever Riley asks to populate/fill/write the email sequence or outreach column, draft Seq 1 / first-touch cold outreach for a named prospect or a batch, crawl the board for cards still needing an email, turn a draft into a LinkedIn message, or continues a run with "keep going" / "next batch" — including voice fragments like "write seq 1 for my accounts" or "draft the cold email for [company]". Handles hook verification, contact checks, fit filtering, compliance holds (fission/HALEU; defense/ITAR; exec-tier routes to Andy), and JE house editorial rules. Not for funding-deadline tracking or ICP scoring (use funding-opportunities-pipeline).
---

# JE Email Sequence 1 — outreach generation & board population

Operating skill for Riley Jackson, sales engineer in BD at Johnston Engineering
(JE), Spokane WA. This skill writes the first-touch cold email (subject +
body) for Riley's accounts and writes it straight onto the **All Accounts**
CRM board. It is the execution arm of the outreach playbook, and it is a
sibling to `funding-opportunities-pipeline` (pipeline, scoring, blue sheets).
This skill does not touch funding boards or ICP scoring.

**The one move.** Every email is a *researched fit hypothesis*, not a
capabilities blast. Take a real trigger, find the specific physical bottleneck
the prospect's technology creates at the stage they are at, and map a named JE
capability to it. If a paragraph could be pasted into an email for a different
company, it is too generic. Cut it.

What JE sells in these emails: mechanical design (SolidWorks), FEA and CFD
(ANSYS), thermal management, electronics packaging, custom hardware
development, fabrication, and build-and-ship. JE also designs and builds at the
core: full electrolyzer stacks from a single cell up, full electrochemical and
battery cells from scratch, separation hardware for critical-mineral
separation, membranes and contactors, and carbon capture systems. JE ships
hardware domestically and internationally.

## Read before working

- `references/style-and-examples.md` — **read before drafting the first email
  in a session.** The matching method, two North Star exemplars, five
  annotated examples (their subject lines, sign-offs, and closing sentence are
  retired — read them for the bottleneck-to-capability move only), the 42-card
  bank of live matches, and the conversion patterns. Find the closest analog
  before writing. This file is mirrored into the
  `funding-opportunities-pipeline` skill; after editing it here, re-copy it
  there so the two do not drift.
- `references/board-mechanics.md` — **read before any monday read or write**
  (crawling for cards, pulling contacts, writing drafts): column IDs, crawl
  filters, Disposition semantics, API landmines, contact-pull recipe, write
  shapes, verify-after-write. A pure drafting request with no board touch can
  skip it.

---

## Scope — whose accounts, which records

- **Riley's accounts only.** Owner column `multiple_person_mm1hxs7c` filtered
  `any_of ["person-95557556"]` (Riley, rileyj@johnstonpe.com). The literal
  `"assigned_to_me"` works too when the call is authenticated as Riley; prefer
  the explicit id for robustness.
- **Suspects and Prospects.** Status column `color_mm1hq3s1`, indexes
  **Suspect = 0, Prospect = 14** (Lead = 103; include only if Riley asks).
- **Never touch other reps' records.** David Tanchin owns a separate
  out-of-scope Suspects set — never touch it. Parker Wilson has some in-scope
  Suspects — a separate pass only if Riley requests it. The owner filter is the
  gate; do not write to a card Riley does not own.

---

## Compliance gate — run FIRST on every card, before drafting

Screen each card fresh; do not rely on a stale hold list. Run it first on the
card as it stands, but two of its three tiers turn on facts that surface only
later — an exec title is verified in the contact step, and a defense or ITAR
nexus often appears during hook research — so an early clear is provisional:
re-apply the screen against what those steps turn up before you stamp the
Disposition. When a hold category plausibly applies and you cannot
affirmatively rule it out, treat it as a hold and route to Andy rather than
clearing it — the cost of a wrong send far exceeds the cost of a delayed one,
so unlike the fit and trigger calls, doubt here resolves toward holding.
Populating a draft column is not sending. The gate controls whether a draft is written at all and,
if written, how it is flagged so nothing gets sent that should not.

- **FULL HOLD — do not draft.** Any fission, radiological, HALEU, nuclear
  fuel-cycle, or NQA-1 flag. Leave the card's placeholder in place, write
  `COMPLIANCE HOLD — needs Andy sign-off (fission/HALEU/etc.)` into fit-notes
  `long_text_mm1t32`, set `Disposition` (`color_mm5830h5`) to `Hold`, and report
  it in the batch summary. (Historically: Urenco USA, Air Products, Sublime
  Nuclear, Hayes Group International, Naval Reactors — re-screen anyway.)
- **DRAFT-BUT-HOLD — draft OK, do not send.** Any defense, military, naval,
  space, orbital, aerospace-platform, ITAR, DARPA, or In-Q-Tel flag. Write the
  draft into subject + body, stamp fit-notes `HOLD for Andy review before send
  (defense/aerospace/ITAR)`, and set `Disposition` to `Hold` (not `Drafted`, so
  it never reads as send-ready). Never present it as send-ready.
- **EXEC-TIER contact — draft, then route.** CEO, co-founder, or C-suite: Andy
  Johnston, P.E. owns these relationships by default. Riley's instruction to
  populate Seq. 1 is the override for the *drafting* step, so write the draft,
  stamp fit-notes `Exec-tier — Andy owns relationship, confirm before send`, and
  set `Disposition` to `Hold`. Riley can redirect any of these.

Defense/aerospace accounts and executive relationships route through Andy
before a send. Keep kill decisions and sends in live chat, not in a scheduled
run. On a gated card the `Hold` value is the only thing between a finished
defense/ITAR or exec draft and a send, so confirm it actually landed before
reporting the card handled rather than trusting the per-batch spot-check — a
draft whose `Hold` silently failed to write has already overwritten its
placeholder, leaving it invisible to both crawls (primary needs the
placeholder, backfill needs an empty body) and sendable by hand.

---

## Fit and contact checks (per card, before drafting)

- **Fit filter.** The prospect must develop novel hardware in-house. Project
  developers, IPPs, operators, and procure-and-deploy integrators are non-fits
  or ecosystem plays only. If a card is a clear non-fit, do not manufacture a
  fit hypothesis — write `FIT MISS — [reason]` to fit-notes, set `Disposition`
  to `Fit-miss`, and flag it in the summary instead of drafting. A large,
  established, EPCM-covered project reduces fit even for a real hardware
  developer; drop to the supplemental-capacity register (below). An "ecosystem
  play" is not a Seq. 1 target either: capture the relationship or referral
  angle in fit-notes and set Fit-miss (or Park if it is worth a later look),
  rather than manufacturing a fit hypothesis for a developer, IPP, or operator
  that builds no hardware in-house.
- **Contact + salutation.** Resolve the account's contact from the All
  Contacts board (recipe in `references/board-mechanics.md`) and verify the
  current title; never assume it from a prior session. When exec-tier
  contacts are linked on a card alongside the engineering target, flag the
  **send blast radius** in fit-notes: if the sequence automation fires to
  every linked contact rather than only the intended one, the CEO gets an
  email written for their engineer — note "verify sequence targets only
  [name]" and name a backup engineering contact where one exists. **Do not write a
  greeting line in the body** — a monday automation prepends "Hi [name]," at
  send, so begin the body at the hook sentence. The PhD-vs-first-name call
  lives on the contact record, not in the body: note in fit-notes when a
  contact holds a PhD so the automation greets them "Dr. [Last name]". The
  contact pull returns only the CRM Title, which is often stale and rarely
  shows a doctorate; confirm the current title and any PhD from the same
  contact research you are already doing (bio, LinkedIn, team page). If you
  cannot confirm either, default to a first-name greeting and flag the
  uncertainty rather than guessing "Dr." If the
  contact sits in HR, finance, legal, comms/PR, or supply chain rather than
  engineering or commercial, add a routing ask rather than pretending they are
  the buyer. If the contact is unverifiable, clearly
  role-mismatched, or entirely absent (empty account_contact), present options
  to Riley rather than drafting. With no linked contact the greeting automation
  has no name to prepend, so a card stamped Drafted would send as "Hi ," — do
  not mark it send-ready.
- **Hook verification.** Verify the hook against a primary or credible source —
  the company's own announcement, an agency/DOE page, a filing, or a reputable
  outlet — not merely any web result; the opening fact is the most visible
  claim in the email, so one you cannot trace to a datable, credible source is
  not verified — treat it as no hook. Never
  fabricate a hook; never use a stale one without flagging it. If a card
  already carries a verified hook in fit-notes, reuse it only if it is still
  current for its type; a verified event can still be stale, so past its window
  re-verify a fresher hook or flag it rather than opening on it. With no strong recent
  hook, fall back to research-discovery framing (weakest tier). If the card is
  stale or thin enough that even research-discovery framing is not warranted, or
  the company cannot be verified, do not draft — set `Disposition` to `Park`,
  note the reason in fit-notes, and flag it. **Tiebreak when both apply:** a
  fit failure outranks a trigger failure — a procure-and-deploy developer with
  no fresh trigger is `Fit-miss`, not `Park`, because the fit problem is
  permanent while the trigger problem is temporal. Congratulations framing only for
  a raise or milestone inside ~6 months; omit funder names and dollar figures.

**Hook hierarchy (use the highest available):** operational milestone
(deployment, commissioning, pilot launch, first unit, production stand-up) >
closed funding round (open with congratulations) > federal program or named
grant > research-discovery framing.

---

## The email — current house style

The structure is three parts: (1) a researched hook paragraph that opens on a
real, verified trigger, (2) a specific fit hypothesis that maps a named JE
capability to the prospect's physical bottleneck, in their own technical
language, and (3) a soft, curious close. Study the two North Star exemplars and
the 42-card bank in `references/style-and-examples.md` and find the closest
analog before writing.

The bottleneck is almost always JE's inference, not something the prospect has
stated, so a claim can be specific and still wrong, and a confidently wrong
engineering claim discredits the whole email to the engineer reading it. Frame
an inferred bottleneck as an informed hypothesis (the I-Pulse "I am partly
guessing where the seams are" move) so the close genuinely invites correction
rather than asserting an engineering fact JE has not verified.

**Capability framing.** Offer the core, the hardware around it, or both: "we
can help with the core reactor itself, the plant around it, or both." Never
wall JE off from the cell or the core hardware in its strong suits
(electrolyzer stacks from a single cell up, electrochemical and battery cells
from scratch, critical-mineral separation hardware, membranes and contactors,
carbon capture systems). **Never** use "stay clear," "steer clear,"
"complement rather than duplicate," or any core-IP boundary hedge — they
undersell JE. The only real IP limit: never claim to copy a prospect's specific
proprietary chemistry, formulation, electrolyte, or design.

**Register by type and size.** In-house hardware developer → full capability
pitch. Peer engineering firm → surge or overflow framing, explicitly not a
suggestion they need help. Established manufacturer or public company →
supplemental capacity on specific programs, additional CFD/FEA capacity,
discrete workstreams, where outside bandwidth helps timelines. Early
pre-hardware → forward-looking and relationship-building. Materials supplier →
the hardware surrounding their material (fixtures, housings, integration), not
the material itself. Software, AI, biology, or chemistry core → say out loud
that their core is not hardware, then position JE around it.

**Firm proof points.** ~30 DOE programs; ~16,000 sq ft Spokane shop across two
buildings (or the single-building ~11,400 sq ft figure when it fits); 800A of
480V three-phase. Use the DOE credential for federal, defense, and DOE-adjacent
prospects; drop it for purely commercial VC-backed startups where it reads
heavy. When a prospect will obviously vet whether JE can actually *build*, add
one named build proof point (see the proof-point bank in the reference file:
Capture6 pilot; OCOchem CO2-to-formate pilot running ~60 tons/year; 29
DOE-funded clean-tech projects in two years).

**Geography.** JE builds and ships hardware domestically and internationally.
Never position a distant or non-US prospect as remote-analysis-only. Full
design-and-build is always on the table; remote delivery is one option, never
the ceiling.

**Close.** Soft, curious, inviting correction. "I would be curious to hear
where X is breaking down for you," "Is this a fair read?" or the cold variant
"does that track with where you're hitting walls?" Use whenever it fits; not
required every time. Never a hard ask.

**Pain-first variant.** When you already know the prospect's specific technical
pain, the highest-converting cold open in the data leads with one concrete
engineering-pain question and a low-friction ask (a 15-minute chat) under a
pain-outcome subject line, instead of a full firm introduction. See Pattern A
in the reference file.

### Editorial rules (hard)

- No em dashes. No bullet points in the body. No comma splices.
- **No greeting line.** Never open the body with "Hi [name]," "Hi there," or
  any salutation. The automation owns the greeting; the body owns everything
  from the hook through the closing question.
- Under ~2,000 characters (LinkedIn hard cap; tighten to ~1,950 on request).
- **No signature block.** End on the closing question.
- **Banned phrase, permanent:** "interested in learning more about your
  development priorities." A finished draft must never contain it. (It remains
  a secondary crawl drop-out signal; `Disposition` is the primary marker of a
  handled card.)
- **Subject line:** unique, custom, tailored to the prospect every time, in
  Title Case (capitalize the principal words). **Never** the old fixed
  "Johnston Engineering - Mechanical Engineering Support for [Company]" format.
  A pain-outcome subject is allowed and often stronger when you know the pain.
- One variant per draft unless Riley asks for options.
- **Emphasis.** The I-Pulse North Star bolds and underlines key lines, but that
  is a warm-follow-up move. Carry it into a cold Seq 1 only if the target
  column actually renders formatting; in a plain-text column it ships as
  literal ** or markup and reads as amateurish, so cold Seq 1 defaults to none.

### Final self-review — run on every draft before it is finished

A draft is not done when it is written; it is done when it survives this
pass. Reread the draft cold and check:

1. **The paste test.** Could the fit-hypothesis paragraph be pasted into an
   email for a different company with only the name swapped? If yes, the
   bottleneck is not specific enough — go back to their actual technology
   and name the physical problem it creates at their stage.
2. **The hook is load-bearing.** The first sentence cites a specific, dated,
   verified event, and the fit hypothesis follows *from it* — not a generic
   pitch wearing a hook as a hat.
3. **Their language, not ours.** The technical terms are the prospect's own
   (their process names, their unit operations), so the reader recognizes a
   peer, not a vendor with a thesaurus.
4. **Register check.** Reread as the recipient: does a peer firm hear "you
   need help"? Does a public company hear a gap pitch instead of capacity?
   Wrong register kills better-researched emails than any other miss.
5. **Mechanical sweep.** No em dashes, no greeting, no signature, no banned
   phrase, no comma splices, subject in Title Case and unique, body under
   ~2,000 characters, paragraphs separated by \n\n.
6. **Fit-notes complete.** Hook + source + date, contact + title verified,
   every flag (PhD greeting, exec-tier linked, blast radius, borderline
   register call) written down — the notes are what makes the next run
   smarter than this one.
7. **Calibration check.** Is any inferred engineering claim stated as flat
   fact? If so, hedge it or pose it as a question.

Fix what fails and re-check. Then, as the last step, confirm the Disposition
matches the compliance gate: a gated draft (compliance, defense/aerospace, or
exec-tier) is `Hold`, never `Drafted` — `Drafted` reads as send-ready and
drops the card from the crawl. Only then stamp.

---

## Writing to the board

Write shapes, batching, and the verify-after-write step are in
`references/board-mechanics.md`. The semantic rule lives here: **after a
clean, Riley-ownable draft** (no compliance flag, non-exec contact), set
`Disposition` to `Drafted` so the card drops out of the crawl. A gated draft
(defense/aerospace or exec-tier) gets `Hold` instead, per the compliance gate.
Resolve the item ID live immediately before the write.

---

## Batch cadence

- Work in batches of **4 to 6 cards per pass.**
- After each batch, produce a structured summary:
  1. **Writes** — company, contact/salutation, and the one-line hook used.
  2. **Holds by reason** — full-hold, draft-but-hold, exec-tier, fit-miss,
     unverifiable/role-mismatch.
  3. **Flagged borderlines** — anything Riley should eyeball.
  Then **stop** and wait for confirmation. "keep going" / "next batch" advances
  the next 4 to 6. Do not re-litigate a settled call; frame a borderline as an
  option once, then execute.
- **Unattended runs.** A scheduled or unattended run has no one to say "keep
  going," so "stop and wait" would strand the queue after batch 1. Instead work
  it in successive batches, emit each summary, and surface — never block on —
  any fit-fail, unverifiable contact, or compliance surprise for Riley's later
  review. Drafting is reversible, so it can run unattended; sending and kill
  decisions are not, so they never do.
- If a contact fails the primary fit filter or is unverifiable, surface it
  rather than pushing a draft. Everything else, correct inline and keep moving.
- **Empty crawl.** If a Disposition-`is_empty` sweep of Riley's
  Suspects/Prospects returns zero, the queue is fully worked — Disposition, not
  body text, is the authoritative handled-marker, so this catches a finished
  draft an earlier run wrote but never stamped, which the placeholder crawl and
  empty-body backfill both miss. Report that cleanly and offer the standing
  next moves: extend into Leads (index 103) only on Riley's say-so, a Parker
  Wilson pass on request, or net-new prospecting via
  `funding-opportunities-pipeline` (Workflow 7). Never loosen the filters to
  manufacture work.

---

## LinkedIn variant (on request)

When Riley says "turn it into a LinkedIn message":

- The compliance gate still applies — and here the Disposition=Hold interlock
  can't back you up, because a LinkedIn message leaves monday and Riley sends it
  by hand. Never hand over paste-ready copy for a full-hold (fission/HALEU)
  account; for a draft-but-hold or exec-tier account, produce it only with the
  hold restated in the same reply (e.g. "HOLD — Andy signs off before this goes
  out"), never as clean send-ready text.
- Open with the hook, then bridge with the exact phrasing "and am reaching out
  to introduce Johnston Engineering as a potential technical resource" (not
  "offering support").
- Compress the capabilities paragraph to "that could mean X, Y, Z, or W." —
  where X/Y/Z/W name work tied to this prospect's actual bottleneck, not JE's
  stock menu; the compression shortens the fit hypothesis, it does not turn it
  back into a capabilities list.
- Keep the same soft close.
- **Omit ANSYS by name** in LinkedIn versions (name it in emails only).
- No em dashes, either surface. Pin the surface first: a cold
  connection-request note is capped near 300 characters, so lead with the hook
  and the ask and cut the rest; an InMail or DM can run longer, but brevity
  still wins there, so treat ~2,000 as a ceiling, not a target.
- The body's no-greeting rule is an email-automation artifact (monday prepends
  the salutation at send); nothing prepends on LinkedIn, so a short greeting is
  natural on a DM or InMail — skip it only when a ~300-char connection note
  leaves no room. Respect the PhD/first-name call from fit-notes.
