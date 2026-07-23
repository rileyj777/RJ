# Workflow 11 — Grant-pursuit brief (one account × one solicitation)

Trigger: "pursuit brief", "grant pursuit brief for {account} on {solicitation}",
"one-pager for {account} + {program}", "how do we play {solicitation} with
{account}", "build the pursuit plan"; also the natural next move whenever
Workflow 1, 6, or 9 surfaces a deadline that lines up with an account.

The board turns funding intel into *awareness*; this workflow turns one
lineup into a *meeting*. It takes one account and one solicitation and
produces a sendable one-pager: the deadline chain, an honest eligibility
read, the teaming structure with JE's scope inside it, and a dated work-back
plan. The brief gives the prospect a reason to get on a call this week — the
deadline does the selling.

**Live chat only.** Never run this scheduled: it produces outbound-facing
material and pairing/eligibility judgment calls belong with the operator.
`references/monday-ids.md` and `references/funding-sources.md` are required
throughout; read `references/style-and-examples.md` only if drafting the
cover note (step 7).

1. **Resolve the pairing.** Pull the funding item from `MY_FUNDING_BOARD`
   (search by solicitation # or name — item-ID snapshots only hold for the
   original board) and the account card from All Accounts (name
   `contains_text`; confirm Owner — another rep's account makes the whole
   brief intel-only for that owner, per ground rules). If the operator named
   only one side, propose up to 3 pairings from the item's Related accounts
   column, the account-clusters map in `references/funding-sources.md`, and
   capability-tag fit — one line of rationale each — and let the operator
   pick before doing the deep work. **Pairing-mode coverage rule:** scan the
   operator's whole book (page until `has_more: false`), not just the first
   pages — a 40%-coverage scan picks the best of what it saw, not the best
   candidate, and must say so if truncated. **Then verify the pick's
   load-bearing rationale before building on it** — if the pairing rests on
   a checkable claim (an early-career PI on staff, a prior award, a pilot
   underway), spend the one web search or sbir.gov lookup that confirms or
   kills it now; a brief built on a deferred "probably" wastes the whole
   run. The winning dossier names at least two independent signals
   (capability fit + a second compelling event such as an award, raise, or
   milestone).

2. **Verify the solicitation at the primary source** (agency page, SAM.gov,
   DSIP, eXCHANGE — not news coverage): open/forecast/closed status, award
   ceiling and period, and the **full deadline chain** — registration
   prerequisites, LOI / concept-paper / Project-Pitch gates, TPOC or Q&A
   cutoff, full-application close **with time-of-day and timezone** (DoW/
   DARPA topics close 12:00 PM ET), and anticipated award date. Every date
   gets "VERIFIED {date}: {source}". A gate already passed can kill the
   pursuit by itself — an invitee-only full application (concept paper or
   LOI already closed) means a non-invitee **cannot apply this cycle**: say
   so plainly and pivot the brief to the next cycle or an adjacent open
   vehicle rather than dressing up a dead run.

3. **Eligibility screen for the account** (fatal flaws first, one verdict
   per line: ✔ pass / ✖ fail / ? needs-check). Size standard and employee
   count; US ownership and the majority-VC rule where the agency allows it;
   foreign-ownership/control/influence (FOCI) disclosures — mandatory on
   every SBIR application since the 2026 reauth (funding-sources.md) and a
   genuine fatal flaw for accounts with foreign founders, investors, or lab
   ties; PI primary-employment rule (SBIR: PI majority-employed by the small
   business; STTR: PI may sit at the research institution); phase logic
   (Phase I vs Direct-to-Phase-II feasibility evidence); topic-specific
   requirements; and **registrations not yet held** — SAM.gov (often 2–6
   weeks, the classic pursuit-killer), SBA registry, and the agency portal
   (DSIP / eXCHANGE / research.gov / eRA Commons, each with its own lead
   time). The brief never asserts eligibility it can't source: a ? verdict
   names exactly what the account must confirm and where. JE is not grants
   counsel — the brief says so in one line.

4. **Structure the teaming play and JE's scope.** Default: the account
   primes, JE is the engineering subcontractor. State JE's allowable share
   from the mechanism — standard SBA guideline: prime performs ≥ 2/3 of a
   SBIR Phase I (subs ≤ 1/3) and ≥ 1/2 of a Phase II (subs ≤ 1/2); STTR
   splits ≥ 40% small business / ≥ 30% research institution with the
   remainder flexible; OTAs and NOFOs carry no SBIR work-share caps —
   **always re-verify against the specific solicitation**, agencies deviate.
   Alternates where they beat the default: JE-teamed STTR with a national
   lab as the research institution (Workflow 9 plays land here);
   license-then-fund (ARPA-E SCALEUP via the Ames→TdVib template); JE-prime
   where the board flags one (⭐). Then name JE's scope the way the outreach
   method does — the specific physical bottleneck the account's technology
   hits inside this solicitation's technical objectives, mapped to a named
   JE capability (DFM, CFD/FEA, build-and-test, pilot fabrication), sized to
   fit the allowable share, with one proof point (the ~30-DOE-programs
   credential earns its keep in a federal brief).

5. **Build the work-back plan** — ≤ 6 dated actions from today to close,
   nearest first: registrations to start now (with lead times), LOI/Q&A
   dates with what to ask through the solicitation's designated channel —
   many DoD/DARPA topics allow direct TPOC contact only pre-release, then
   route questions anonymously through SITIS once the topic opens, so a plan
   that says "email the TPOC" on an open topic advises a rule violation that
   can cost the account — internal draft and red-team dates, and submission
   ≥ 48 hours before the deadline
   (portals fail at the buzzer). Flag noon-ET closes in the plan, not just
   the chain.

6. **Compliance gate before anything is sendable** (same gate as
   `je-outreach-seq1`; a brief is not a send). Fission / HALEU / nuclear
   fuel-cycle account: **internal-only** — build the brief for Andy's
   review, never format it for the prospect. Defense / aerospace / ITAR
   account *or* solicitation (most DoD and DARPA topics qualify): draft the
   full brief but stamp it "HOLD — Andy review before send" and never
   present it as send-ready. Exec-tier recipient: Andy owns the
   relationship — flag the routing. Also respect export-control basics in
   the *content*: a brief for a foreign-owned account never proposes an
   ITAR-touching scope.

7. **Assemble the one-pager** using this exact structure (it must actually
   fit one page — roughly 350–500 words; the digest carries anything that
   doesn't):

   ```
   GRANT-PURSUIT BRIEF — {Account} × {Program / Topic #}
   {date} · Johnston Engineering · prepared by {operator}
   STATUS: {send-ready | HOLD — Andy review before send | INTERNAL-ONLY — do not send}

   THE OPPORTUNITY — mechanism, office, award ceiling + period, one line on
   what it funds and why this account's technology is a fit (2–3 lines).

   DEADLINE CHAIN — table: Gate | Date | Note. Registrations (lead times),
   LOI/concept gate, Q&A cutoff, close (time + timezone), expected award.

   ELIGIBILITY SNAPSHOT — ✔/✖/? per requirement, one line each; ? lines say
   what to confirm and where. One-line disclaimer: verify against the
   official solicitation; JE is not grants counsel.

   THE TEAMING PLAY — who primes; JE's scope and named capability inside
   the allowable work share; one proof point; alternate structure if one
   genuinely competes.

   WORK-BACK PLAN — ≤ 6 dated actions, nearest first.

   SOURCES — primary links, each with its VERIFIED date.
   ```

   Offer a .docx render (docx skill) when the operator wants it
   prospect-ready. The step-6 verdict rides in the STATUS line at the top of
   the brief, not only in the chat, so a held or internal-only brief keeps
   its stamp when exported — only a send-ready brief is prospect-ready. A
   cover note on request: read
   `references/style-and-examples.md` first — hook = the deadline chain
   ("the Q&A window closes {date}"), house voice, soft close, and the
   je-outreach-seq1 editorial rules apply to the note (not to the brief's
   tables).

8. **Board writes — propose, then write on the operator's go:** funding
   item Stage → `Pursuing` (`color_mm569kc0`) only on a go or gated-live
   verdict. A pursuit killed in step 2/3 does not get `Pursuing` — set
   Stage → `Passed` (a real option) or leave as-is, and re-bucket to
   Watchlist against the next-cycle close date per step 10, so downstream
   WF6/WF10 don't resurface a dead lane as active. Append the account to
   Related accounts (`text_mm56tvrb` — overwrites, rewrite old + new); add
   a Notes line "Pursuit brief {date}: {account} — {sent/held/internal}".
   On the account card, log an update (comment), not a column write. If the
   pairing was operator-picked in step 1, these writes are what make the
   next Workflow 6 brief remember it.

9. **Gated pursuits get branch plans, not a verdict alone.** When the go/
   no-go turns on a fact the operator must obtain (invitee status, a filed
   abstract, a license in hand), the brief structures all branches so JE
   wins on any answer: *yes* → the dated sprint plan is ready to execute;
   *no* → the next-cycle or adjacent-vehicle play plus the relationship
   move that books the meeting anyway; *unknown* → the single question to
   ask, worded so asking it is itself a credible touch. The deadline opened
   the conversation; the conversation is the point.

10. **Digest:** the pairing and its verdict (go / gated / dead-this-cycle),
    the single nearest gate date, eligibility ?-items the account must
    answer, compliance holds applied, and where the brief landed (sent /
    held for Andy / internal-only). If the pursuit died in step 2 or 3, the
    digest names the next cycle date or the adjacent vehicle to watch —
    a dead pursuit should still leave a breadcrumb on the Watchlist. State
    book-scan coverage when the pairing was proposed rather than named.
