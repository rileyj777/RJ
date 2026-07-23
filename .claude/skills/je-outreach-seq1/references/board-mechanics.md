# Board mechanics — crawl, contact pull, write shapes

Read this before any monday.com read or write in a session (crawling for
cards, pulling contacts, or writing drafts/dispositions). The editorial and
compliance rules stay in SKILL.md; this file is the plumbing.

## Pre-flight (before any writing in a session)

1. **Confirm the monday connection is live** and the board is reachable.
2. **Read board structure live** with `get_board_items_page`
   (`includeColumns: true`) and confirm the Seq. 1 columns still exist with
   these IDs before you write to them:
   - Subject → `text_mm1kyzgk`
   - Body → `long_text_mm1ka0r6`
   - Fit / flag notes → `long_text_mm1t32`
3. **Crawl for cards that still need an email.** AND-filter,
   `filtersOperator: "and"`, `limit: 50`, `includeColumns: true`:
   - `multiple_person_mm1hxs7c any_of ["person-95557556"]`
   - `color_mm1hq3s1 any_of [0, 14]` (Suspect / Prospect) — these are
     positional label indices that shift if labels are reordered or inserted,
     so confirm they still map to Suspect/Prospect in the step-2 live column
     read before crawling; otherwise the crawl could silently retarget cold
     outreach onto the wrong stage (e.g. Won/Dead cards).
   - `color_mm5830h5 is_empty`
   - `long_text_mm1ka0r6 contains_text "interested in learning more about your development priorities"`
4. **Resolve item IDs live, immediately before writing** each card. Never
   reuse an item ID from memory or a prior turn.
5. **Name-collision traps** on this board — confirm you have the right card:
   "Nanoramic" sits inside NORAM, "Starstone" / "thestarstone" inside STARS
   Technology, "Nextech Batteries" inside NexTech. Resolve which sibling you
   have by exact item-name match plus the account link, not a
   `searchTerm`/fuzzy lookup — substring matching can return the neighbor or
   skip the exact card.

## Disposition semantics (`color_mm5830h5`)

**Disposition is the primary marker of a handled card.** Any value means the
card has been dealt with and it drops out of the crawl; `is_empty` keeps the
crawl to cards that still need a decision or a draft. Labels:

- `Drafted` — a clean, Riley-ownable draft was written (normal review/send).
- `Hold` — must go through Andy before it moves: a full compliance hold (not
  drafted), or a gated draft (defense/aerospace draft-but-hold, or exec-tier).
- `Fit-miss` — screened out on fit; no draft.
- `Park` — real but no current trigger, or unverifiable; revisit later.
- `Kill` — confirmed dead/defunct; never draft.
- empty — still needs a decision or a draft (this is the crawl set).

A crawled card that already carries a dated decision in fit-notes (PARK, FIT
MISS, hold language) with no Disposition was decisioned by an earlier run that
never stamped it: set the matching Disposition from the note rather than
re-working the card, unless the note is stale or contradicted by fresh facts.

The placeholder-phrase rule is a secondary signal: a finished draft overwrites
the placeholder with real copy, so it also drops out that way. If a batch of
Riley's cards has empty bodies rather than the placeholder, run a second
backfill pass with the same owner + stage + `color_mm5830h5 is_empty` filters
plus `long_text_mm1ka0r6 is_empty` as the fourth condition, and skip any body
that already reads as a finished email. (Once every historical draft is
backfilled to `Drafted`, the placeholder rule can be retired and the crawl
becomes Disposition-only.)

## API mechanics, learned live

- The `get_board_items_page` response nests the payload: the outer result
  holds a `text` field that is itself a JSON string, so parse twice (or walk
  the structure recursively to find the `items` list) rather than indexing
  the top level.
- Cursors expire fast — on a cursor error, restart the crawl from page 1 with
  the same filters; already-written cards fall out on their own.
- Cursor pages after the first drop `column_values` (IDs and names only), so
  when column data matters, re-run the filtered query instead of paginating
  deep.
- The filtered set can exceed a page (278 cards in July 2026): work from
  page 1 in batches, since stamped cards fall out of the filter and the front
  page refreshes itself.

## Contact pull (All Contacts board `7253021389`)

Resolve the account's contact via the `contact_account` link (Title is
`text_mm22r0k0`). The reliable pull is `get_board_items_page` on `7253021389`
with `itemIds` taken from the account card's `account_contact` field and
`columnIds: ["text_mm22r0k0"]`. Do **not** filter that board by
`contact_account any_of [account ids]` — it returns zero rows even for linked
contacts; the `contains_text "<account name>"` form works but only one account
per query.

**Greeting mechanism (why the body carries no salutation):** a monday
automation prepends "Hi [name]," at send. The RJ sequence resolves on the
Contacts board through mirror columns that pull the account-side Subject and
Seq. 1 down via `contact_account`; First Name comes from the contact record
itself. The PhD-vs-first-name call therefore lives on the contact record, not
in the body: note in fit-notes when a contact holds a PhD so the record and
automation greet them "Dr. [Last name]".

## Write shapes

- Subject → `text_mm1kyzgk` (plain string, or `{"name": "..."}`-style value
  per the column's write shape). Body → `long_text_mm1ka0r6` as
  `{"text": "..."}`. Flags/notes → `long_text_mm1t32` as `{"text": "..."}`.
- **Paragraphs in the body are separated by `\n\n`.**
- Write per-card with `change_item_column_values`, or batch with a single
  `all_api_write` mutation using short aliased variables. JSON-variable
  payloads with quotes have errored before; since the copy carries no em
  dashes this is low-risk, but on any `Variable ... invalid value` error fall
  back to the dedicated `change_item_column_values` tool per card.
- Disposition write shape: `{"color_mm5830h5": {"label": "Drafted"}}` through
  `change_item_column_values` stores cleanly; `change_simple_column_value`
  with the plain label string (e.g. `value: "Drafted"`) also works and is the
  fallback.
- **Verify after writing.** Re-fetch every card written in the batch, not
  just a sample — the aliased single-mutation batch path can partially apply
  or map one card's copy onto another card's item. Confirm each card carries
  its own intended subject and body (the hook you researched for that account,
  not a neighbor's) and that its Disposition flipped to Drafted before
  reporting the batch done; a quick scan for quoting artifacts still applies.
