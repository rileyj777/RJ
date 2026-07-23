# monday.com IDs & recipes (Johnston Engineering)

**Operator identity (self-scoping).** This skill is shared across JE BD on
the same boards. At the start of any CRM workflow, call monday
`get_user_context` once and capture `MY_USER_ID` (the current operator's
monday user id) and `MY_EMAIL`. Wherever this file shows `<MY_USER_ID>`,
substitute that value at runtime — never hardcode a person's id.
CRM workspace id `7757951`; funding board workspace id `7310246`.

## Funding Opportunity Pipeline — per-operator boards

Each BD operator now has their own copy of this board (identical structure and
items). Resolve the operator's board in Step 0 as `MY_FUNDING_BOARD` and use it
for every funding-board operation (Workflows 1, 2, 6). Map by `MY_USER_ID`:

| Operator | user id | `MY_FUNDING_BOARD` |
|---|---|---|
| Riley Jackson | 95557556 | `18421616108` (original / shared) |
| Parker Wilson | 73250064 | `18421966525` |
| David Tanchin | 78522796 | `18421966586` |
| Austin Stone | 27429080 | `18421966599` |
| Shane Greenfield | 104666598 | `18421966606` |

If `MY_USER_ID` isn't in this table (new operator), search boards for
"Funding Opportunity Pipeline - <their name>" and use that id; if none exists,
fall back to `18421616108` and tell them their board isn't set up yet. All
copies share the group/column schema below: board duplication preserves the column
IDs (confirmed on the copies) and the group IDs. If a Workflow 1 group-move
ever errors on a copy, re-pull that board's group IDs. **The item-ID snapshot further down is for the original board
`18421616108` only** — on any other board, resolve items by search
(solicitation # or name), never by those ids.

URL (original): https://johnston-engineering.monday.com/boards/18421616108

### Groups (deadline buckets)
| Group | ID |
|---|---|
| 🔴 Closing <2 weeks | `group_mm56tkfw` |
| 🟠 2–6 weeks | `group_mm56cw3d` |
| 🟡 6 weeks–3 months | `group_mm56ccg3` |
| 🔵 Watchlist / rolling / TBD | `group_mm56nn69` |
| 🧪 Lab tech & licensable IP | `group_mm565gts` |
| 🏛️ State programs | `group_mm56v4mf` |
| 📚 Source directory | `group_mm56z8xs` |

### Columns
| Column | ID | Notes |
|---|---|---|
| Source | `dropdown_mm56p15g` | DoD/DoW, DARPA, ARPA-E, DOE, NSF, NIH, USDA, National Labs, State, Corporate |
| Mechanism | `dropdown_mm56v84x` | SBIR/STTR Ph I, SBIR/STTR Ph II, Grant/NOFO, Prize, License, OTA |
| Solicitation # | `text_mm56k1r1` | |
| Opens | `date_mm56tyrh` | |
| Closes | `date_mm56x0zr` | drives group placement |
| Fit | `color_mm56rp3p` | High / Medium / Low |
| Stage | `color_mm569kc0` | New / Reviewing / Pursuing / Submitted / Won / Passed |
| Award $ | `text_mm563pp3` | |
| Link | `link_mm56tg60` | `{"url":..., "text":...}` |
| Notes | `long_text_mm56tg73` | `{"text": "..."}`; prefix verified facts "VERIFIED {date}:" |
| Related accounts | `text_mm56tvrb` | plain text; **overwrites** — rewrite full string when appending |

### Key opportunity item IDs (July 2026 snapshot — original board `18421616108` only)
DoD wave 7/22 `12511970230` · DoD wave 8/19 ⭐JE-prime `12511970249` ·
DARPA SBIR ExCAIPE+MANTRAS (7/22 noon) `12512058888` · DARPA BTO BAA (9/30)
`12512059043` · DARPA ExPEDitions (8/19, DARPA-PS-26-118) `12512064990` ·
DARPA Smash (verify) `12512099517` · SBIR Strategic Breakthrough Awards
`12512075946` · ARPA-E SCALEUP Ready (rolling) `12511970252` · ARPA-E NOFO
DE-FOA-0003105 `12511958888` · DOE CMMA TA3 (7/23) `12511970091` · DOE SBIR
Ph I FY27 `12511970020` · NSF (9/5; invited full 11/4) `12511994613` · NIH
(9/8) `12512008700` · USDA (TBD) `12511960257` · ISC Canada `12511970092` ·
Argonne ACCESS `12511969978` · NLR `12511969982` · TechLink `12511970021` ·
CMI Hub `12511970114` · CMI magnet-recovery machinery patent `12512059042` ·
CMI Li-ion leach patent `12512034003` · CMI electrorefining portfolio
`12512034004` · American-Made prizes `12512009796` · Halliburton Labs
`12512010013` · Shell GameChanger `12512091257`.

State items: CO OEDIT `12512055100`, CA CalSEED `12512054910`, NY NYSERDA
`12511975225`, WA CEF `12511979285`, PA BFTP `12511979574`, MN Launch MN
`12511974952`, MT `12511979575`, FL HighTech `12512055196`, NM NMSBA
`12511975226`, NV GOED `12511974964`, OR `12511979355`, WY `12511975005`,
ID IGEM `12511975006`, WV `12511979354`.

## All Accounts — board `7253021439` (~2,880 items)

| Column | ID | Notes |
|---|---|---|
| Owner | `multiple_person_mm1hxs7c` | filter `any_of ["person-<MY_USER_ID>"]` for your book |
| Status | `color_mm1hq3s1` | indexes: Suspect=0, Prospect=14, Lead=103 |
| Industry | `dropdown_mm1sga1v` | |
| Capability fit tags | `dropdown_mm1h5y5v` | drives Industry Fit pre-score |
| Location | `location_mm1hwpre` | drives state-program matching |

**Your-book pull recipe:** `get_board_items_page` with filters
`[{multiple_person_mm1hxs7c any_of ["person-<MY_USER_ID>"]},
{color_mm1hq3s1 any_of [0,14,103]}]`, operator `and`, limit 60, slim
columnIds `[color_mm1hq3s1, dropdown_mm1sga1v, dropdown_mm1h5y5v,
location_mm1hwpre]`. Book size varies per operator; page with the cursor
until `has_more: false`. Cursors expire ~60 min — on cursor error, restart
from page 1 with the same filters.

## All Contacts — board `7253021389` (~9,231 items)

| Column | ID | Notes |
|---|---|---|
| Title | `text_mm22r0k0` | |
| Seniority Tier | `dropdown_mm22qz3v` | auto-classified from title |
| Email | `contact_email` | check domain vs company! |
| Buying Influence | `dropdown_mm525a5g` | labels seeded: Economic Buyer, Technical Buyer, User Buyer. "Coach" not yet created — create via `create_labels_if_missing` only when the operator explicitly assigns one |
| Account link | `board_relation` `contact_account` | **the only way to filter to your contacts** |
| Account Owner (mirror) | `lookup_mm1jyqjg` | ⚠ NOT filterable via API |

**Contacts pull recipe:** filter `contact_account any_of [<account item
IDs>]`, columnIds `[contact_account, text_mm22r0k0, dropdown_mm22qz3v,
contact_email, dropdown_mm525a5g]`.

### Tagged buying influences
Per-operator output of Workflow 3 — not shared skill state. Each operator
builds their own buying-influence map on their own accounts (Economic /
Technical / User Buyer tags via the recipe above); a Coach is never
auto-assigned.

### Standing data-quality flags (shared CRM — verify, extend as you find more)
Shared-board issues any operator touching the account should know; confirm
before acting:
- **Safire**: CRM contacts are Safire *Insurance* (South Africa) — wrong
  company vs. the defense-battery Safire. Do not sequence.
- **GaNify**: contact Yixin Xiong has a google.com email — verify.
- **Jetti**: "Director of Instructor Training" title suggests a wrong-company contact.
- **Zero-contact accounts** are uncovered bases (a Miller-Heiman red flag);
  each operator tracks their own from Workflow 6.

**Whole-CRM dedupe recipe (Workflow 7):** for each shortlist finalist, run
`get_board_items_page` on `7253021439` with a name `contains_text` filter
(try the short name / no-suffix variant too), `limit: 3`,
`includeColumns: false`. Do **not** use `searchTerm` for dedupe (landmine 9),
and do not page through the book or CRM — per-finalist queries cover it. Any
hit anywhere in the CRM — regardless of owner — disqualifies the add; note
owned-elsewhere matches separately. A `contains_text` hit is a candidate,
not proof — the filter over-matches, so a short or common finalist name (a
3–4-char token or a dictionary word) collides with unrelated cards and would
falsely drop a real net-new add. On a hit, re-pull that item with Owner +
Industry/Location: enough to confirm it's the same company (not a namesake —
cf. the Safire *Insurance* vs defense-battery Safire flag) and to read the
Owner that step 4's owned-elsewhere clause and step 5's near-miss routing
both need. `includeColumns:false` stays fine when nothing matches.

**New-suspect creation recipe (Workflow 7, only on the operator's go):**
`create_item` / `create_items` on `7253021439` with columnValues:
`{"color_mm1hq3s1":{"label":"Suspect"},
"multiple_person_mm1hxs7c":{"personsAndTeams":[{"id":<MY_USER_ID>,"kind":"person"}]},
"dropdown_mm1sga1v":{"labels":["<existing industry>"]},
"dropdown_mm1h5y5v":{"labels":["<existing capability tags>"]}}` —
keep `createLabelsIfMissing` **false** here (use the existing taxonomy; don't
invent tags on a shared board). Stamp provenance: put
`"Added by Claude prospecting {date} — source: {where found}"` in the first
update/comment on the item, and put the HQ city there too if you skip the
location column (see landmine 8).

## API landmines (learned the hard way)

1. **Mirror/lookup columns cannot be filtered** through `items_page` — filter
   through the underlying `board_relation` column instead.
2. **`all_api_write` JSON variables**: long strings with em-dashes/quotes have
   errored ("Variable $x of type JSON! was provided invalid value"). Keep
   variables short and reusable (e.g., one `$eco` per role, aliased across
   items), or fall back to the dedicated `change_item_column_values` tool.
3. **Moving groups** needs a `move_item_to_group` mutation via `all_api_write`
   — `change_item_column_values` can't do it. Batch it with column updates
   only if the variables are simple.
4. **Text columns overwrite** — to append to "Related accounts", write the
   full old+new string.
5. **Dropdowns**: `{"labels": ["..."]}` with `createLabelsIfMissing: true`
   creates missing labels (needs board-structure permission).
6. **DoW/DARPA SBIR topics close at 12:00 PM ET** — surface "noon" in Notes
   and digests so nobody plans for 11:59 PM.
7. **Item names** can be set via `change_item_column_values` with
   `{"name": "..."}`.
8. **Location columns need coordinates** — the API value is
   `{"lat": "...", "lng": "...", "address": "..."}`; a plain city string
   fails. When creating suspects without coordinates, skip the location
   column and record the HQ city in the item's first update instead.
9. **`searchTerm` hides exact matches** — its relevance ranking can return
   only fuzzy neighbors for a full-name query (observed: "Infinite Elements"
   returned other "Elements" cards but not the exact one), producing false
   net-new adds. Use a name `contains_text` filter for dedupe and existence
   checks; reserve `searchTerm` for exploratory lookups.
