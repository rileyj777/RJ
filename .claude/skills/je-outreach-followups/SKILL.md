---
name: je-outreach-followups
description: Triage replies to Johnston Engineering outreach and draft the follow-up on Riley Jackson's accounts — classify what came back (interested, question/objection, not-now, wrong-person, negative) or handle silence with new-angle bumps, then write the response in JE house voice and log state to the monday.com All Accounts board (7253021439). Use whenever Riley pastes or mentions a prospect reply, asks "what do I say back", "follow up with [company]", "no response from [company]", "bump [company]", "check for replies", asks how to answer an objection like "we have engineers in-house", wants a LinkedIn follow-up, or says "they wrote back". Handles the objection playbook (in-house team, too-early/no-budget, cost asks, send-more-info), funding-deadline bumps, meeting-ask replies, compliance holds (fission/HALEU; defense/ITAR; exec-tier routes to Andy), and reply-thread editorial rules. Not for first-touch cold outreach (je-outreach-seq1) or funding tracking (funding-opportunities-pipeline).
---

# JE Follow-ups — reply triage & next-touch drafting

_v1.2 — sibling to `je-outreach-seq1` (first touch) and
`funding-opportunities-pipeline` (deadlines, pipeline). Seq1 opens the
conversation; this skill keeps it alive. (v1.1 added the funding-hook card,
downstream CRM-state reads, and send-mailbox forensics; v1.2 makes the
funding card an active board pull rather than an optional decline, and adds
the out-of-office rule — both from iteration-2 validation.)_

Operating skill for Riley Jackson, sales engineer in BD at Johnston
Engineering (JE), Spokane WA. A reply is the scarcest asset in the funnel —
minutes of good judgment here are worth more than a week of new cold sends.

**The one move.** Answer their exact words first — the question they actually
asked, in their technical language, within the first two sentences — then
offer exactly one concrete next step. Never re-pitch the firm to someone who
already read the pitch; a reply thread is a conversation, not a second
brochure.

## Read before working

- `references/style-and-examples.md` — read before drafting the first
  follow-up in a session: JE house voice, the bottleneck-to-capability
  method, exemplars, the 42-card bank, conversion patterns. Follow-ups
  inherit the voice; find the closest analog before writing.
- Board mechanics are inline below (this skill is self-contained on column
  IDs so it works even when `je-outreach-seq1` isn't loaded).

## Scope — whose accounts, which records

Riley's accounts only: All Accounts board `7253021439`, Owner column
`multiple_person_mm1hxs7c` filtered `any_of ["person-95557556"]`. Never touch
another rep's records; an inbound reply on someone else's account is
intel-only for that owner. Contacts live on All Contacts `7253021389`
(filter through `contact_account`; Email `contact_email`, Title
`text_mm22r0k0`).

Key columns on All Accounts:

| Column | ID | Use |
|---|---|---|
| Disposition | `color_mm5830h5` | labels: Drafted(1) / Hold(0) / Undecided(9) / Fit-miss(17) / Park(106) / Kill(2) |
| Reach Out Notes | `long_text_mm1t32` | the running log — hooks, holds, reply state. Long-text **overwrites**: read current text, append, write back old+new |
| 🤖 Email Subject | `text_mm1kyzgk` | Seq-1 subject (do not overwrite on replies — replies keep the thread) |
| 🤖 Email Seq. 1 | `long_text_mm1ka0r6` | the first-touch body that prompted the reply — read it before drafting |
| ⚙️ Email Seq. 3 | `text_mm1h6vh2` | later-sequence slot |
| Email | `email_mm533p2n` | the send-target address on the item |
| ☀️ LinkedIn Contacted / Date | `boolean_mm31dp2z` / `date_mm317nq3` | channel history |

**Send-pipeline reality (verified 2026-07-20 — re-check before relying on
it):** the board's "RJ" sequence (4 auto-email steps, days 1/4/7/10) has
never completed a send — its recorded runs all terminated
`no_recipient_email` because the enrolled item's Email column was empty. It
resolves its recipient from the item's own Email column, i.e. one address
per item, not every linked contact. But emails HAVE gone out through other
paths (manual sends, other enrollments — the sending mailbox is on the
hyphenated johnston-pe.com domain, easy to miss replies on) and have drawn
replies. Per-account send state is messy, so never assert what was or
wasn't sent from memory or from this note: the account's Emails &
Activities timeline is the source of truth, checked per account. Delete
this note when the pipeline is verified clean.

## Intake — two ways work arrives

1. **Riley pastes or describes a reply** ("Bardo wrote back: …", a forwarded
   email, a screenshot). Trust the text; resolve the account card and
   contact from the boards; read the Seq-1 draft and Reach Out Notes so the
   follow-up knows what the prospect was responding to.
2. **"Check for replies" sweep.** Pull inbound signals from the monday
   Emails & Activities timeline on Riley's accounts and from HeyReach
   (LinkedIn) conversations — resolve both toolsets via tool search on first
   use. If either system is unreachable, say so in the first line and state
   which channel's replies are therefore invisible; a sweep built from one
   channel must never read as if it covered both. List who replied, classify
   each (below), and work them as a batch.

**Read the downstream state, not just the card.** monday auto-actions fire
on replies and clicks: a contact can flip to "Success! Move to Leads," a
lead card can spawn on the Leads board with a task ("schedule intro
meeting"), and sequence enrollments terminate on click or reply. Before
deciding a next touch, pull these — lead cards, tasks, and
sequence-enrollment status — so you see what already happened automatically
and don't propose a touch the system (or Riley's earlier self) already made.
A reply that already got a scheduling response is a *meeting to confirm*,
not a reply to draft.

## Compliance gate — run FIRST on every reply, before drafting

An inbound reply never lifts a hold; it makes the hold matter more, because
now there's momentum behind the send.

- **FULL HOLD (fission / radiological / HALEU / nuclear fuel-cycle / NQA-1):**
  do not draft a prospect-facing reply. Summarize the reply and draft
  talking points for Andy; log the hold in Reach Out Notes.
- **DRAFT-BUT-HOLD (defense / military / space / aerospace platform / ITAR /
  DARPA / In-Q-Tel):** draft the reply, stamp Reach Out Notes `HOLD for Andy
  review before send`, set Disposition `Hold`, never present it send-ready.
- **EXEC-TIER sender (CEO / founder / C-suite replied):** Andy owns the
  relationship. Draft the reply for continuity plus a two-line heads-up to
  Andy; Riley decides who sends. Stamp the routing in Notes.
- Never explain a hold to the prospect; compliance reasoning stays internal.

## Triage — classify, then run the play

Classify each reply as the single best fit and run its play. Speed matters:
a positive reply deserves a same-day draft.

**1. INTERESTED / meeting ask.** Reply in 2–4 sentences: confirm the scope
in their words, offer two specific times (or Riley's scheduling link), stop
selling — the meeting is the close now. Log `REPLIED {date}: positive —
{gist}; proposed {times}` to Notes. Suggest running call-prep before the
meeting if that skill/context is available. Propose (don't create) a
`Replied` or `Meeting` Disposition label — creating labels on the shared
board is a one-time Riley decision; until then Disposition stays `Drafted`
with the state carried in Notes.

**2. QUESTION / OBJECTION.** Run the objection playbook (next section).
Answer first, evidence second, ask last.

**3. NOT-NOW ("circle back in Q4", "post-raise", "after the pilot").**
Thank them, one line that keeps the door open, and — when the board shows a
real one — name the concrete event that will restart the thread ("we'll
watch for the pilot commissioning"). Set Disposition `Park`, log `REPLIED
{date}: not-now until {date/trigger}` so the funding skill's relationship
pulse resurfaces it on time.

**4. WRONG-PERSON ("talk to our ops lead").** Thank them and ask for the
intro in the same breath — a warm handoff beats a cold restart. In parallel,
resolve the named person (All Contacts, then web) and verify their title. If
no intro comes, the follow-up to the new contact opens with the routing
("{Name} suggested I reach you"). Log the redirect; Disposition stays
`Drafted` while the thread is live.

**5. NEGATIVE / unsubscribe.** No counter-pitch, ever. If a courteous
one-liner is warranted, keep it to one line. Log `REPLIED {date}: negative —
{gist}`; propose Disposition `Kill` but never set it yourself — kill
decisions belong to Riley in live chat.

**6. SILENCE (no reply).** **Verify the silence before bumping.** "No
response" is the trigger to check, not a fact to build on: pull the
account's Emails & Activities timeline and the LinkedIn/HeyReach thread
first. Do the **root-cause forensics**, not just a binary bounced/replied:
check which mailbox and domain the send went from (JE runs both
`johnstonpe.com` and the hyphenated `johnston-pe.com`; a reply can land in
one inbox while Riley watches the other), and read the actual send, bounce
(NDR), and reply timestamps. Report *why* it looked silent — that is what
stops the same false-silence next time. A bounced first touch (dead
address) means fix the contact and re-send touch 1 properly, not a bump;
retire the dead address but keep the person flagged on the card as a
possible future contact rather than deleting them. A reply already sitting
in the thread, or a scheduling reply Riley's own mailbox already sent,
means this is not silence: triage it above and tell Riley what actually
happened. **An out-of-office / auto-reply is neither engagement nor a
bounce** — it is a paused clock. When Riley reports one (or you find one),
treat his stated return date as authoritative input even if the CRM record
doesn't show it: **reset the effective no-reply clock to the return date**
and count business days from there, not from the original send. So an OOO
"back the 14th" seen on the 20th is ~4 business days of real silence, not
two-plus weeks — usually too early for the +5–7-day bump. If the board
record and Riley's account of the send conflict, surface the mismatch as a
data-hygiene flag rather than disputing his premise. Only an intact send
with a genuine, clock-elapsed no-reply enters the bump cadence. A bump must carry **new information** — a fresh
verified trigger, a relevant funding deadline, a named build proof point, or
a sharper question. "Just checking in" and "bumping this to the top of your
inbox" are banned as the *substance* of a touch. The JE-native bump: pull
the account's lane deadline from the funding board ("DOE CMMA TA3 closes
{date} — the test-stand scope we mentioned is exactly what that money
funds") — verify the date before using it, and if the account sits in
another operator's funding-board territory, use only Riley's own board.
Cadence: bump 1 at +5–7 business days from the send; bump 2 at +2–3 weeks
with the value-add; then Park with a dated re-check. Alternate channels:
if two emails went quiet and the LinkedIn columns show no touch, propose
one LinkedIn message (je-outreach-seq1 has the LinkedIn variant rules —
introduce-as-resource bridge, no ANSYS by name, under 2,000 chars).

## Objection playbook — patterns, not scripts

Find the closest analog in the reply bank before writing; these are the
recurring shapes and the JE-true counters. One proof point per reply, max.

- **"We have engineers in-house."** Agree sincerely — that's who JE works
  *with*, not around. Reframe to the discrete workstream from the Seq-1
  hypothesis: surge capacity on a bounded deliverable (a test stand, a CFD
  campaign, DFM on one assembly), not staff augmentation. Peer-firm register
  rules apply: never imply they need help.
- **"Too early / no budget."** The non-dilutive counter is JE's home turf:
  name the live solicitation in their lane from Riley's funding board with
  its verified close date, and frame JE's scope as what that money funds.
  Offer the forward-relationship version if nothing is live: "worth 15
  minutes now so we're not starting from zero when the award lands."
- **"What would it cost?"** Never quote numbers in a reply thread. Scope
  first: propose the 15-minute call to bound the workstream, and describe
  engagement shape qualitatively (discrete fixed-scope workstreams vs.
  ongoing analysis support) so the call feels safe to take.
- **"Can you actually do X?"** Answer honestly from JE's capability list —
  including "that part we wouldn't take on" when true; honesty about edges
  converts better than coverage claims. Never claim the prospect's
  chemistry, formulation, or proprietary design; JE builds the hardware and
  systems around it.
- **"Send more info."** One tailored paragraph plus the single most relevant
  proof point (Capture6 pilot; OCOchem CO2-to-formate pilot at ~60 t/yr; ~30
  DOE-funded programs), then the call ask. A deck dump is a dead thread.

## Funding-hook card — the deal lever, kept out of the body

JE's edge is that a live non-dilutive deadline is a reason to talk *now*, so
this is an **active step, not an optional afterthought**. On every reply and
every bump, actually **pull Riley's Funding Pipeline board** (`MY_FUNDING_BOARD`
= `18421616108`) and screen it for a program that fits the account's lane —
match on the capability/cluster tags the way the funding skill does. Do the
pull; do not skip it because the reply "isn't about budget." The card rides
along on *every* follow-up because a live deadline is a reason to talk
regardless of what the prospect asked.

Then print a **Funding-hook card** section below the draft with one of three
honest outcomes — never a fourth option of silently omitting it:

1. **A live fit** — name the program, its verified close/next gate date and
   source, and the one-line JE angle. This is an optional card the SE can
   weave in; it never becomes a second ask inside the send-ready body (that
   breaks the one-ask rule and the word cap).
2. **A do-not-raise → say why** — flag any program the account should NOT be
   pitched, with the reason: a passed gate ("DOE Critical Minerals TA3 — LOI
   gate closed April, do not raise this cycle") *or* a technical non-fit
   ("DARPA ExCAIPE requires electrically rechargeable cells — Hybrium's tech
   is chemically refueled, do not raise"). Naming the reason stops the same
   dead runway being pitched next time. This negative check is half the value.
3. **Board pulled, nothing live fits** — say exactly that ("checked
   `MY_FUNDING_BOARD`, no open program fits {account}'s lane right now"). This
   is a valid outcome; "I could pull it if you want" is **not** — the whole
   point is that you already did.

Never surface a program from memory — pull it or say the board was
unreachable. If a genuine pursuit lines up (account × live solicitation),
point Riley at `funding-opportunities-pipeline` Workflow 11 (grant-pursuit
brief) rather than building the whole pursuit here — this skill owns the
reply, that skill owns the pursuit.

The "too-early / no budget" objection is where the card most often becomes
the *substance* of the answer; elsewhere it rides along as a sweetener — but
the board pull happens either way.

## The reply — editorial rules (differ from Seq1 where marked)

- **Greeting line IS included** (unlike Seq-1 drafts, where the automation
  prepends it): "Hi {first name}," — or "Dr. {last name}" when the contact
  record flags a PhD.
- Keep the thread: replies go under the existing subject (`Re: …`). Never
  invent a new subject for a reply; a bump on a dead thread may re-use the
  original subject or a sharper pain-outcome variant — that's the one
  exception.
- Short wins in-thread: target ≤120 words for replies, ≤80 for bumps. If the
  answer genuinely needs more, propose the call instead of writing the memo.
- No em dashes. No bullet lists in the body. No comma splices. No signature
  block (Riley's mail client owns it) — end on the question or the ask.
- Banned phrase stays banned: "interested in learning more about your
  development priorities."
- One draft per reply unless Riley asks for options; frame a borderline
  call as an option once, then execute.

## Final self-review — every draft, before it's finished

1. **Did I answer their exact words?** Quote-check: the first two sentences
   must connect to what they actually wrote, not to what we wish they'd asked.
2. **New information?** (Bumps only) — name the new fact; if there isn't
   one, the bump isn't ready to send.
3. **Register check.** Reread as the recipient — does a peer hear "you need
   help"? Does an exec get a junior-sounding note?
4. **Mechanical sweep.** Greeting present and correct form; no em dashes; no
   banned phrase; word cap; thread subject preserved; no signature.
5. **Compliance stamped.** Hold state and Andy routing recorded where they
   apply; nothing gated presented as send-ready.
6. **Notes complete.** Reply class + date + gist + next trigger logged so
   the next run (and the Monday relationship pulse) is smarter than this one.

## Writing to the board

Resolve the item ID live immediately before any write. Reach Out Notes is
long-text and **overwrites** — read the current value, append the new dated
line, write the full old+new text. Disposition transitions this skill may
set directly after a clean draft: `Park` (not-now, exhausted bumps) and
`Hold` (compliance). `Kill` and any new label creation are propose-only.
Never write to the Seq-1 subject/body columns from this skill — those
belong to je-outreach-seq1; follow-up drafts live in the chat response and
in Notes.

## Batch cadence

Work replies singly on demand; sweeps in batches of 4–6. After each batch:
**Drafts ready** (account, class, one-line gist), **Holds by reason**,
**Cadence set** (parks with dates), **Flagged borderlines**. Then stop —
"keep going" advances the next batch. End every run with a short digest:
what's drafted awaiting Riley's send, what's held for Andy, what's parked
with dates, and which channels the sweep could not see.
