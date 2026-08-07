#!/usr/bin/env python3
"""Deterministic checker for the mechanical JE Seq. 1 editorial rules.

Checks only what a machine can settle: em dashes, greeting lines, signature
blocks, the banned phrase, character count, Title Case subjects, paragraph
separation. It never rewrites copy.

What it deliberately does NOT check, because these need judgment and belong to
the model's final self-review: the paste test, whether the hook is
load-bearing, whether the technical language is the prospect's own, register,
comma splices, and whether a subject is genuinely tailored rather than merely
capitalized.

Usage:
    lint_draft.py --subject "Subject Line Here" --body-file draft.txt
    lint_draft.py --subject "..." --body-file - < draft.txt
    lint_draft.py --body-file draft.txt          # body-only checks

Exit codes: 0 all passed, 1 one or more FAILs, 2 bad invocation.
"""

import argparse
import re
import sys

MAX_CHARS = 2000
TIGHT_CHARS = 1950

BANNED_PHRASES = [
    "interested in learning more about your development priorities",
]

RETIRED_SUBJECT = re.compile(
    r"johnston\s+engineering\s*-\s*mechanical\s+engineering\s+support\s+for",
    re.I,
)

GREETING = re.compile(
    r"^\s*(hi|hello|hey|dear|greetings|good\s+(morning|afternoon|evening))\b",
    re.I,
)

# A sign-off counts only when it is the whole line, so an in-sentence "Best" or
# "Thanks for" does not trip the check. Matched anywhere in the body rather than
# only in the tail: a standalone "Best," line is wrong wherever it appears, and
# a tail-only check misses it whenever anything follows the signature.
SIGNOFF = re.compile(
    r"^\s*(best|regards|best\s+regards|thanks|thank\s+you|cheers|sincerely|"
    r"warmly|all\s+the\s+best|talk\s+soon)\b[\s,.!-]*$",
    re.I,
)

# Title Case: these may stay lowercase unless first or last word.
SMALL_WORDS = {
    "a", "an", "and", "as", "at", "but", "by", "for", "from", "in", "into",
    "nor", "of", "on", "onto", "or", "over", "per", "the", "to", "up", "via",
    "vs", "with", "yet",
}

DASHES = {"—": "em dash", "–": "en dash", "―": "horizontal bar"}


class Report:
    def __init__(self):
        self.rows = []

    def add(self, ok, name, detail=""):
        self.rows.append((ok, name, detail))

    def emit(self):
        failed = 0
        for ok, name, detail in self.rows:
            tag = "PASS" if ok else "FAIL"
            if not ok:
                failed += 1
            line = f"[{tag}] {name}"
            if detail:
                line += f": {detail}"
            print(line)
        total = len(self.rows)
        print(f"\n{total - failed}/{total} checks passed.")
        return failed


def check_subject(subject, rep):
    if RETIRED_SUBJECT.search(subject):
        rep.add(False, "subject/retired-format",
                "uses the retired 'Johnston Engineering - Mechanical "
                "Engineering Support for [Company]' format")
    else:
        rep.add(True, "subject/retired-format")

    bad_dash = [n for ch, n in DASHES.items() if ch in subject]
    rep.add(not bad_dash, "subject/no-em-dash",
            f"contains {', '.join(sorted(set(bad_dash)))}" if bad_dash else "")

    words = [w for w in re.split(r"\s+", subject.strip()) if w]
    offenders = []
    for i, w in enumerate(words):
        core = w.strip("\"'()[],.:;!?")
        if not core or not core[0].isalpha():
            continue
        # An all-caps token is an acronym (GWh, MILAbot, DOE), not a case error.
        if core.isupper() or any(c.isupper() for c in core[1:]):
            continue
        if core[0].islower():
            if i not in (0, len(words) - 1) and core.lower() in SMALL_WORDS:
                continue
            offenders.append(core)
    rep.add(not offenders, "subject/title-case",
            f"lowercase principal word(s): {', '.join(offenders)}"
            if offenders else "")


def check_body(body, rep, tight):
    stripped = body.strip()

    found = [n for ch, n in DASHES.items() if ch in body]
    rep.add(not found, "body/no-em-dash",
            f"contains {', '.join(sorted(set(found)))}" if found else "")

    first = stripped.splitlines()[0] if stripped else ""
    rep.add(not GREETING.match(first), "body/no-greeting",
            f"opens with a salutation: {first[:48]!r}"
            if GREETING.match(first) else "")

    sig = [ln.strip() for ln in stripped.splitlines() if SIGNOFF.match(ln)]
    rep.add(not sig, "body/no-signature",
            f"standalone sign-off line: {sig[0][:48]!r}" if sig else "")

    hits = [p for p in BANNED_PHRASES if p in body.lower()]
    rep.add(not hits, "body/banned-phrase",
            f"contains banned phrase: {hits[0]!r}" if hits else "")

    limit = TIGHT_CHARS if tight else MAX_CHARS
    n = len(body)
    rep.add(n <= limit, "body/length",
            f"{n} chars, over the {limit} limit by {n - limit}"
            if n > limit else f"{n} chars (limit {limit})")

    paras = [p for p in stripped.split("\n\n") if p.strip()]
    rep.add(len(paras) >= 2, "body/paragraph-breaks",
            "no blank-line paragraph separation found; monday needs \\n\\n"
            if len(paras) < 2 else f"{len(paras)} paragraphs")

    lone = [ln for ln in stripped.splitlines()
            if re.match(r"^\s*([-*•]|\d+[.)])\s+", ln)]
    rep.add(not lone, "body/no-bullets",
            f"{len(lone)} bullet or numbered line(s) in body" if lone else "")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--subject", default=None)
    ap.add_argument("--body-file", default=None,
                    help="path to the body text, or - for stdin")
    ap.add_argument("--tight", action="store_true",
                    help=f"use the {TIGHT_CHARS}-char limit instead of "
                         f"{MAX_CHARS}")
    args = ap.parse_args()

    if args.subject is None and args.body_file is None:
        ap.error("pass --subject, --body-file, or both")

    rep = Report()
    if args.subject is not None:
        check_subject(args.subject, rep)
    if args.body_file is not None:
        try:
            if args.body_file == "-":
                body = sys.stdin.read()
            else:
                with open(args.body_file, encoding="utf-8") as fh:
                    body = fh.read()
        except OSError as exc:
            print(f"error: cannot read body file: {exc}", file=sys.stderr)
            return 2
        check_body(body, rep, args.tight)

    return 1 if rep.emit() else 0


if __name__ == "__main__":
    sys.exit(main())
