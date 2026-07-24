# Workflow 13 — Proposal-kickoff handoff (won pursuit → scoped JE proposal)

Trigger: "proposal kickoff for {account}", "scope a proposal for {account}",
"turn this pursuit into a proposal", "{account} said yes — start the proposal",
"won {account}"; the natural next move after Workflow 11 lands a go/won or a
prospect reply converts (the Pattern E motion in `style-and-examples.md`).

This is the **bridge** between the funding/BD pipeline and JE's proposal work —
it assembles the inputs and produces a *scoped proposal skeleton* plus the
information request that unblocks pricing. It is **not** a full proposal writer
and it **does not price.**

**Live chat only; assemble + propose, Riley finalizes.** It produces
client-facing material and rests on scoping judgment, so it is never scheduled
(same class as WF11/WF12). Only your own accounts (Owner == `MY_USER_ID`).
`references/monday-ids.md` and `references/style-and-examples.md` are used
here; **the proposal standards themselves live in the root `CLAUDE.md`** —
read it and follow it exactly rather than restating or forking it here (same
single-source discipline as the scoring taxonomy).

1. **Assemble the inputs.** Pull the account card (All Accounts; confirm
   ownership — a teammate's account makes this intel-only). If the proposal
   ties to a solicitation, pull the funding item (`MY_FUNDING_BOARD`) and reuse
   the **WF11 pursuit brief** if one exists — its bottleneck→capability scope,
   teaming structure, and eligibility read are already done. Capture the
   conversion context: what did the prospect actually agree to (intro call
   held? scope discussed? which subsystem)? Note where they sit in the Pattern
   E rhythm — intro call → same-day recap → NDA → technical interchange with
   **Andy Johnston, P.E.** engineer-to-engineer → PFD/process-model ask →
   pricing → proposal → negotiation.
2. **Name the scoping artifact JE needs before it can price** — per Pattern E,
   the PFD / process model with flow rates is the artifact Andy needs to scope
   and price. If it is not in hand, the kickoff's primary output is the
   **request for it** plus a clean numbered action list (the same-day-recap
   move), **not** a finished proposal. Do not scaffold a scope or pricing
   against unknowns.
3. **Draft the proposal skeleton to the JE standards in `CLAUDE.md`** (section
   order; SOW Key-Tasks order; the two-subsection Deliverables; Exclusions and
   IP templates; Project Timeline structure; billing model; phrasing
   conventions incl. **no em dashes**). Build structure from
   `reference/templates/` (JE's own templates/examples). Pull the *technical*
   scope — the Background project-example fit and the SOW's core work — from
   the pursuit brief / the outreach bottleneck-to-capability match
   (`style-and-examples.md`), so the SOW is scoped to the account's specific
   physical bottleneck, not generic capability language.
4. **Do not price. Ever, here.** Per `CLAUDE.md`, Riley owns and manages all
   pricing figures; never compute, fill, reconcile, or "correct" T&M /
   Fixed-Fee / materials-markup / sales-tax numbers. Mark the Cost Summary
   table and the Baseline Hardware List `[Riley to price]` and stop. The
   standing rate facts (T&M rate, 25% markup, 9.1% tax, Fixed-Fee = T&M × 1.25)
   are Riley's to apply, not the workflow's.
5. **Honor the mandatory exclusions** (`CLAUDE.md`): never insert prior-art /
   patent-review / literature-review / background-research scope in any form;
   default to pressure-decay testing, not helium leak testing. Apply the
   Exclusions and IP-Rights templates verbatim.
6. **Compliance gate before anything is client-facing** (same gate as
   `je-outreach-seq1` / WF11; a draft is not a send). Fission / HALEU /
   nuclear-fuel-cycle account → **internal-only**, build for Andy, never format
   for the prospect. Defense / aerospace / ITAR account or scope → draft but
   stamp "HOLD — Andy review before send." Exec-tier recipient → Andy owns the
   relationship; flag the routing.
7. **Render on request** via the `docx` skill using `reference/templates/` as
   the base; the compliance status rides in the document, not just the chat.
8. **Log on monday (propose, write on the go):** account update "Proposal
   kickoff {date}: {scope one-liner} — {sent / held / internal}"; if
   solicitation-tied, note it on the funding item and set Stage as appropriate.
9. **Digest:** what was assembled, the scoping artifact still needed (usually
   the PFD ask), that pricing is left to Riley, the compliance status applied,
   and where the kickoff landed.
