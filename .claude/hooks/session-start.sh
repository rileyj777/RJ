#!/bin/bash
# SessionStart hook for the JE BD/proposal repo.
#
# Two jobs:
#   1. Sync this repo's JE skills over the account-installed copies, so a
#      session loads what is on main rather than whatever was last uploaded
#      to the Claude account. Without this the two drift: Workflow 1 writes
#      its refreshed deadline snapshot into the repo, but the next session
#      loads the uploaded copy and reads a stale baseline. That happened on
#      2026-08-07, when the loaded skill was three weeks behind main.
#   2. Install the Python deps so pytest and flake8 work without a manual
#      pip install first.
#
# REMOTE ONLY. The skill sync writes into $HOME/.claude/skills, which in a
# remote container is a throwaway copy downloaded at container start. On a
# local machine that same path holds the real personal skills, and clobbering
# them would be destructive, so the whole hook no-ops off the web.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  echo "session-start: not a remote session, skipping (local ~/.claude/skills is not ours to overwrite)"
  exit 0
fi

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
SRC="$PROJECT_DIR/.claude/skills"
DEST="${HOME}/.claude/skills"

# Skills this repo owns. Anthropic-managed skills (docx, pdf, pptx, xlsx,
# skill-creator, morning, ...) live in the same directory and are never touched.
JE_SKILLS="funding-opportunities-pipeline je-outreach-seq1 je-outreach-followups"

# ---------------------------------------------------------------------------
# 1. Sync repo skills -> account-installed copies
# ---------------------------------------------------------------------------
# Non-fatal: a sync problem should never stop the session from starting.
sync_skills() {
  if [ ! -d "$SRC" ]; then
    echo "session-start: no $SRC, nothing to sync"
    return 0
  fi
  if [ ! -d "$DEST" ]; then
    echo "session-start: no $DEST (skills not installed here), skipping sync"
    return 0
  fi

  local backup_root="${HOME}/.claude/skills-backup"

  for skill in $JE_SKILLS; do
    if [ ! -d "$SRC/$skill" ]; then
      echo "session-start:   - $skill not in repo, skipped"
      continue
    fi

    # Is the account copy already identical to the repo? Then do nothing, so a
    # no-op session start stays silent and cheap.
    if [ -d "$DEST/$skill" ] && diff -r -q \
         --exclude='__pycache__' --exclude='*.pyc' --exclude='.pytest_cache' \
         "$SRC/$skill" "$DEST/$skill" >/dev/null 2>&1; then
      echo "session-start:   - $skill already in sync"
      continue
    fi

    # The account copy differs. It may be NEWER than the repo (an upload that
    # has not landed on main yet, or another session's in-flight work), so never
    # discard it silently - stash a copy first and say so. Repo still wins, but
    # the overwritten version stays recoverable for the life of the container.
    if [ -d "$DEST/$skill" ]; then
      mkdir -p "$backup_root"
      rm -rf "${backup_root:?}/$skill"
      cp -a "$DEST/$skill" "$backup_root/$skill" 2>/dev/null || true
      echo "session-start:   - $skill DIFFERED; account copy backed up to $backup_root/$skill"
    fi

    rm -rf "${DEST:?}/$skill"
    mkdir -p "$DEST/$skill"
    # -a to preserve modes; exclude build/test cruft that should never ship
    if command -v rsync >/dev/null 2>&1; then
      rsync -a --delete \
        --exclude '__pycache__/' --exclude '*.pyc' \
        --exclude '.pytest_cache/' --exclude '.DS_Store' \
        "$SRC/$skill/" "$DEST/$skill/"
    else
      cp -a "$SRC/$skill/." "$DEST/$skill/"
      find "$DEST/$skill" \( -name '__pycache__' -o -name '.pytest_cache' \) \
        -type d -prune -exec rm -rf {} + 2>/dev/null || true
      find "$DEST/$skill" -name '*.pyc' -delete 2>/dev/null || true
    fi
    echo "session-start:   - synced $skill from repo"
  done
}

echo "session-start: syncing repo skills into $DEST"
if ! sync_skills; then
  echo "session-start: WARNING - skill sync failed; session continues with the account copies" >&2
fi

# ---------------------------------------------------------------------------
# 2. Python deps (matches what .github/workflows/python-package.yml installs)
# ---------------------------------------------------------------------------
install_deps() {
  # Deliberately no `pip install --upgrade pip`: on this image pip is
  # Debian-packaged and the self-upgrade fails with "RECORD file not found".
  # It is noise, it is not needed to install anything below, and because
  # `set -e` is suspended inside a function called from an `if`, a failure
  # there would have been swallowed rather than reported.
  python3 -m pip install --quiet --disable-pip-version-check flake8 pytest || return 1
  if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    python3 -m pip install --quiet --disable-pip-version-check \
      -r "$PROJECT_DIR/requirements.txt" || return 1
  fi
  # Prove the install actually worked rather than trusting the exit code.
  python3 -c 'import openpyxl, pytest' >/dev/null 2>&1 || return 1
}

echo "session-start: installing Python deps"
if ! install_deps; then
  echo "session-start: WARNING - dependency install failed; pytest/flake8 may be unavailable" >&2
fi

echo "session-start: done"
