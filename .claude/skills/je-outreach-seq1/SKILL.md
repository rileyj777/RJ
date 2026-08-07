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
- `references/contact-discovery.md` — load **only when a card has an empty or
  unusable `account_contact`.** Finds an engineering-tier contact, creates the
  record on All Contacts `7253021389`, links it to the account card.
- `references/qa-sweep.md` — load **only when running a pre-send QA pass** over
  already-stamped cards. Read-only audit; never drafts.
- `scripts/lint_draft.py` — deterministic checker for the mechanical editorial
  rules (em dashes, greeting line, signature block, banned phrase, character
  count, Title Case subject). Run it on every draft instead of eyeballing those
  rules by hand. It is a linter, not an editor: it never rewrites copy.

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

- **Fit filter (calibrated inclusive — default to drafting).** The bar is a
  plausible mechanical/hardware hook, not a purity test. If the prospect builds,
  scales, assembles, integrates, or even just specifies real physical hardware
  or process equipment, it is a **fit** — draft it, with the register adjusted
  (see below). Drafts are reviewed before send and never auto-fire, so a
  marginal draft is cheap while wrongly killing a live prospect is expensive:
  **when in doubt, draft.** This explicitly includes categories an older,
  stricter reading wrongly treated as non-fits: procure-and-deploy
  **integrators** and full-service design-build-operate shops (draft around the
  skid packaging, enclosure, thermal, and DFM work, not the commodity unit ops);
  **assemblers** of packaged or containerized systems (draft around enclosure,
  cooling, structural, and container-level mechanical design); utility-scale and
  infrastructure **project developers / IPPs** (draft around the mechanical
  subsystems and pressure/flow/structural hardware they still have to engineer);
  and **resource / minerals developers** standing up a first-of-a-kind pilot or
  process plant (draft around process-vessel design, mixing/CFD, and pilot
  hardware scale-up). A software, biology, or chemistry **core** is likewise a
  draft, not a miss — acknowledge the core and position JE around the
  surrounding hardware (the Endolith move). Reserve `Fit-miss` for genuine
  non-fits only: a pure software / AI / services / branding play with no
  physical hardware to engineer at all; and `Kill` for a confirmed dead or
  defunct account or a duplicate card. Never fabricate a hook or a hardware
  angle that is not there. A large, established, or EPCM-covered player is still
  a fit but shifts to the supplemental-capacity register (below). Calibration
  anchors (Riley, 2026-07-23, all confirmed **fit** over a stricter first pass):
  Epic CleanTec (water-reuse integrator), FENECON USA (BESS assembler), Rocky
  Mountain Power / RMP (CAES + hydro project developer), Geophysx Jamaica
  (red-mud REE resource developer building a FOAK pilot).
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
  the buyer. If the contact is unverifiable or clearly role-mismatched, present
  options to Riley rather than drafting. With no linked contact the greeting
  automation has no name to prepend, so a card stamped Drafted would send as
  "Hi ," — do not mark it send-ready.
- **Empty `account_contact` is the common case, not an edge case.** On a
  freshly sourced batch most cards carry no linked contact at all (11 of 12 in
  the 2026-08-07 crawl). Treat it as a step in the pass, not a reason to stop:
  run the **contact-discovery workflow** in
  `references/contact-discovery.md`, which finds an engineering-tier contact,
  creates the record on All Contacts `7253021389`, and links it back. If
  discovery fails, still draft (drafting is reversible and the research is the
  expensive part), stamp `Hold`, and write `NO LINKED CONTACT — not enrollable,
  greeting automation would send "Hi ,"` into fit-notes. Never stamp `Drafted`
  on a card with no linked contact.
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
- **When the source page will not load (fetch-blocked environments).** In a
  sandboxed or proxied environment a direct fetch of the primary source often
  fails outright: in the 2026-08-07 run, 5 of 6 fetches came back
  `EGRESS_BLOCKED` (activate.org, news.mit.edu, prnewswire.com, apidaeforms.com,
  houston.innovationmap.com). A blocked fetch is **not** a failed
  verification, and it is not a licence to relax the bar either. The fallback
  standard: the hook is verified when **two or more independent sources**
  surface it with a **specific date** and the details agree across them, and at
  least one is the primary announcement or a reputable outlet rather than an
  aggregator. Record in fit-notes which domains were blocked and that
  confirmation came from search-result content rather than a direct fetch, and
  say so in the batch summary so the fact carries a known confidence level.
  One undated source, or two that trace to the same press release with
  conflicting details, is still no hook.

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

**Funding-partner angle (add when a real funding fit exists).** When the
prospect's technology plausibly aligns with a current non-dilutive funding
opportunity (SBIR/STTR, DOE FOA, ARPA-E, a DoD topic, or a relevant state or
agency grant), name it and offer JE as a proposal partner: JE would join as a
subcontractor to help them win the award and support the proposal, so the
engineering is funded by the program rather than out of their pocket. Frame it
as free, non-dilutive money they are well positioned to capture, backed by JE's
federal track record (about 30 DOE programs, 29 DOE-funded clean-tech projects
in two years) as proof JE is a credible proposal teammate. Only raise it when
the alignment is real and the program plausibly open; never invent a
solicitation. This also brings the DOE credential back into play for an
otherwise commercial prospect. Keep it to one or two sentences inside the body,
never a second full pitch. For defense or ITAR-adjacent programs the
draft-but-hold gate still applies. (Cross-reference the
`funding-opportunities-pipeline` skill for live solicitations when scoping the
fit.)

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
5. **Mechanical sweep — run the linter, do not eyeball it.**
   `python3 scripts/lint_draft.py --subject "..." --body-file <path>` checks em
   dashes, greeting line, signature block, banned phrase, character count,
   Title Case, and paragraph separation deterministically, and exits non-zero
   on any failure. It is cheaper and more reliable than re-reading for
   punctuation, and it frees your attention for checks 1 through 4 and 7, which
   are the ones that actually need judgment. Two things the linter cannot
   judge, so they stay manual: comma splices and whether the subject is
   genuinely *tailored* rather than merely capitalized.
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

## Pre-send QA sweep (on request, or before Riley enrolls a batch)

A read-only audit over already-stamped cards, run when Riley asks to check the
book before sending or says some variant of "is this batch ready to go."
Procedure is in `references/qa-sweep.md`. It exists because the two failures
that actually reach a prospect are silent ones: a gated draft whose `Hold`
never landed, and a `Drafted` card with no linked contact that sends as
"Hi ,". Both are invisible to the drafting crawl, because any Disposition value
drops a card out of it.

The sweep never drafts, never sends, and never changes copy. It reports, and
Riley decides. The one write it may make is correcting a Disposition that
contradicts its own fit-notes (a note reading `HOLD for Andy` on a card stamped
`Drafted`), and it names every such correction in the summary.

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
