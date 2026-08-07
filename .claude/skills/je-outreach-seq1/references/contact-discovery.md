# Contact discovery — finding and linking an engineering contact

Load this only when a card has an empty or unusable `account_contact`. On
freshly sourced batches this is the common case, not an edge case: 11 of the 12
cards in the 2026-08-07 crawl had no linked contact at all.

Why it matters mechanically: a monday automation prepends "Hi [name]," at send,
resolving First Name from the **contact record**. With no linked contact there
is no name to prepend and the email ships as "Hi ,". A card with no contact is
therefore never `Drafted`, however good the copy is.

## Order of work

Do discovery **after** the fit and hook checks pass, not before. Roughly half of
crawled cards end up `Park`, `Fit-miss`, or full-hold, and contact research on a
card that is never going to be drafted is pure waste.

## Who to look for, in priority order

The target is the person who owns the physical problem the email describes.

1. **Engineering leadership** — VP/Director/Head of Engineering, CTO at a
   company small enough that the CTO is still hands-on, Chief Engineer.
2. **The named technical person from the hook itself.** If the trigger was a
   paper, a conference talk, a patent, or a lab program, the author or
   presenter is both the best-matched reader and proof the research is real.
   This is the strongest option when it exists.
3. **Programme or product engineering** — Director of Product/Programs,
   manufacturing or process engineering lead at a company standing up a line.
4. **Founder/CEO only at genuinely small companies** (roughly under 20 people),
   where they are the engineer. This is exec-tier: it routes to Andy and the
   card is stamped `Hold`, per the compliance gate in SKILL.md.

Skip HR, finance, legal, comms/PR, and supply chain. If the only findable
contact sits in one of those, the draft needs a routing ask rather than a
pretend-buyer framing, and the card stays `Hold`.

## Sourcing the name

Company team/leadership page, the hook source itself (press releases usually
quote an executive and sometimes a technical lead), LinkedIn, conference
programmes, patent assignee/inventor records, university or lab lab-group pages
for spinouts. Accelerator profiles (Activate, HAX, Silicon Catalyst) reliably
name founders.

**Verify the title is current.** The CRM Title field is often stale and rarely
shows a doctorate. Confirm both the title and any PhD from the same research
pass, and record the PhD in fit-notes so the record greets them "Dr. [Last
name]". If you cannot confirm either, default to first name and flag it. Never
guess "Dr."

**Do not invent an email address.** Guessed-pattern addresses bounce, and a
bounce burns the sending domain for every other account on the board. Create
the record with the name and title, leave email empty, and flag in the batch
summary that the address still needs sourcing. Bounced sends are already a
tracked status on the board (`Bounced (SPAMED)`), which is the cost of getting
this wrong.

## Writing the contact record

All Contacts board is `7253021389`. Title column is `text_mm22r0k0`; the link
back to the account is `contact_account`.

1. **Check for an existing record first.** Query All Contacts with
   `contains_text "<account name>"` against `contact_account` (the
   `any_of [account ids]` form returns zero rows even for genuinely linked
   contacts, so do not use it). One account per query. A contact may already
   exist unlinked, and creating a duplicate is worse than leaving it empty.
2. **Create with `create_item`** on `7253021389`: item name is the person's
   full name, `text_mm22r0k0` is the verified title, `contact_account` links to
   the account item id.
3. **Confirm the link resolved from the account side** by re-reading the
   account card's `account_contact`. The link is what the sequence automation
   traverses; a contact created but not linked is invisible to it.
4. **Record it in fit-notes**: name, title, where the title was verified and on
   what date, PhD status, and whether an email address is still outstanding.

## When discovery fails

Do not stall the card and do not manufacture a name. Draft anyway if fit and
hook pass, since the research is the expensive part and drafting is reversible.
Then stamp `Hold`, write `NO LINKED CONTACT — not enrollable, greeting
automation would send "Hi ,"` into fit-notes along with any partial leads found,
and surface it in the batch summary. It is a finished draft waiting on one
field, which is a much better resting state than an unworked card.
