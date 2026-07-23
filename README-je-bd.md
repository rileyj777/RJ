# Johnston Engineering BD — Claude Code project

This is your JE BD/proposal Claude Projects setup repackaged for Claude Code: the standards and
context that were living in Claude's memory, plus your three custom monday.com skills, plus your
own proposal templates.

## Setup

1. Unzip this into a folder and `cd` into it (or `git init` it as its own repo — either works;
   Claude Code picks up `CLAUDE.md` and `.claude/skills/` from the directory you start it in).
2. Start Claude Code in that folder. It will automatically load `CLAUDE.md` and discover the
   three skills under `.claude/skills/`.
3. Connect the monday.com MCP server (see below) — the skills won't work without it.
4. Optional: set up a document-editing tool (see below) if you want to edit .docx proposals
   directly in Claude Code the way you have been in claude.ai.

## What's included

| Path | What it is |
|---|---|
| `CLAUDE.md` | Durable proposal standards, pricing rules, phrasing conventions, company facts — the equivalent of what was in Claude's memory for this project. |
| `context/active-engagement-recovered-potential.md` | Snapshot of the current Recovered Potential deal. Deal-specific, meant to be replaced/updated as work progresses — don't treat it as a standard. |
| `.claude/skills/je-outreach-seq1/` | Cold-outreach Sequence 1 drafting for the monday.com All Accounts board (first touch). |
| `.claude/skills/je-outreach-followups/` | Reply triage + next-touch drafting (v1.2): classify the reply or handle silence, draft the response, log state. Keeps the thread alive after seq1. |
| `.claude/skills/funding-opportunities-pipeline/` | Funding pipeline, CRM, and Strategic Selling workflows (v4.2, 11 workflows). |
| `reference/templates/` | Your own JE proposal templates and past proposal examples, copied from Claude Projects knowledge. |
| `reference/docx-editing-notes.md` | Gotchas learned from editing JE proposal .docx files — notes only, not a tool (see below). |

### Note on the superseded Strategic Selling skill

Earlier bundles shipped a second skill, `je-strategic-selling` (v3.1), that overlapped
`funding-opportunities-pipeline`. It has since been superseded: `funding-opportunities-pipeline`
v4.2 is the single source of truth for the funding pipeline, CRM, and Strategic Selling
workflows (it absorbed everything `je-strategic-selling` did and added the grant-pursuit brief,
Workflow 11). `je-strategic-selling` is no longer packaged here. If a copy is still installed in
claude.ai, remove it from the claude.ai skill settings so the two don't both trigger.

## Gap: document-editing tooling

Anthropic's own Word/PDF/PowerPoint/Excel editing skills (used automatically in claude.ai) are
under license terms that don't allow extracting or redistributing their files outside Anthropic's
services — so this repo can't include a copy of the exact tool you've been using in claude.ai.
`reference/docx-editing-notes.md` captures the *patterns and gotchas* specific to your documents,
but not the actual scripts.

To get equivalent .docx editing capability in Claude Code, you have a few options:
- Check whether your Claude Code / Anthropic plan now offers an official installable Skill for
  this (this has been in flux — check `docs.claude.com` or ask Claude Code directly, since this
  may have changed since this was written).
- Have Claude Code write its own unpack/edit/repack scripts on the fly per session (works, but
  redoes work each time).
- Use a general-purpose Node.js library like `docx` for building new proposals from
  `CLAUDE.md`'s standards, which sidesteps raw XML editing entirely for net-new documents (only
  raw XML editing needs the unpack/repack approach — editing an *existing* file).

## Setting up the monday.com MCP connector

All three skills call monday.com tools. In Claude Code, MCP servers are configured per-project
or globally (not automatically inherited from claude.ai). Check the current syntax in
`docs.claude.com` (Claude Code → MCP), since flags/commands change — as of this writing it's
generally something like:

```
claude mcp add --transport http monday https://mcp.monday.com/mcp
```

You'll need to complete monday.com's OAuth/connection flow the first time, same as you did in
claude.ai.

## Keeping this current

- When a deal wraps or a new one starts, update or add files under `context/` — don't let stale
  deal state accumulate in `CLAUDE.md`.
- If your proposal standards change (rates, section order, exclusions), edit `CLAUDE.md` directly
  — that's now the single source of truth instead of Claude's memory.
- If you revise a skill in claude.ai later, re-copy its folder into `.claude/skills/` here to
  keep them in sync (there's no automatic sync between the two).
