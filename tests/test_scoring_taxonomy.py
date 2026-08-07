"""Contract tests for scoring_taxonomy.json.

The taxonomy is the canonical scoring model for the funding-opportunities-pipeline
skill (build_workbook.py reads it; references/funding-sources.md mirrors it by
hand). These tests lock the parts that are easy to break silently, because a
scoring regression does not crash anything - it just quietly mis-ranks accounts.
"""
import json
import re
from pathlib import Path

import pytest

TAXONOMY_PATH = (
    Path(__file__).resolve().parents[1]
    / ".claude/skills/funding-opportunities-pipeline/scripts/scoring_taxonomy.json"
)


@pytest.fixture(scope="module")
def tax():
    with TAXONOMY_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def test_taxonomy_file_exists():
    assert TAXONOMY_PATH.is_file(), f"canonical taxonomy missing at {TAXONOMY_PATH}"


def test_required_keys_present(tax):
    required = [
        "keyword_tiers",
        "junk_terms",
        "bullseye_tags",
        "adjacent_tags",
        "industry_fit_valid_industries",
        "icp_weights",
        "normalize_suffix_terms",
        "score_include_threshold",
        "prequalified_force_include",
        "fuzzy_cutoff",
    ]
    missing = [k for k in required if k not in tax]
    assert not missing, f"build_workbook.py reads these keys; missing: {missing}"


def test_keyword_tiers_are_5_4_3_and_non_empty(tax):
    assert set(tax["keyword_tiers"]) == {"5", "4", "3"}
    for tier, terms in tax["keyword_tiers"].items():
        assert terms, f"tier {tier} is empty"


def test_every_pattern_compiles(tax):
    """A bad fragment would be silently dropped at build time, costing a tier."""
    bad = []
    for tier, terms in tax["keyword_tiers"].items():
        for t in terms:
            try:
                re.compile(t)
            except re.error as e:
                bad.append(f"tier {tier}: {t!r} ({e})")
    for t in tax["junk_terms"]:
        try:
            re.compile(t)
        except re.error as e:
            bad.append(f"junk: {t!r} ({e})")
    assert not bad, "uncompilable taxonomy patterns: " + "; ".join(bad)


def test_icp_weights_match_documented_defaults(tax):
    """SKILL.md v4.2.2 fixed these weights; drift here changes every ICP score."""
    assert tax["icp_weights"] == {
        "Industry Fit": 1.0,
        "Company Size Fit": 1.0,
        "Compelling Event Present": 2.0,
        "Access to Economic Buyer": 1.5,
        "Growth/Follow-On Potential": 1.0,
    }


def test_thresholds_are_coherent(tax):
    """Pre-qualified lists force-include at a HIGHER bar than the general one."""
    assert tax["score_include_threshold"] == 3
    assert tax["prequalified_force_include"] == 4
    assert tax["prequalified_force_include"] >= tax["score_include_threshold"]
    assert 0 < float(tax["fuzzy_cutoff"]) <= 1.0


def test_bullseye_and_adjacent_tags_do_not_overlap(tax):
    """A tag in both lists would score as bullseye and adjacent at once."""
    overlap = set(t.lower() for t in tax["bullseye_tags"]) & set(
        t.lower() for t in tax["adjacent_tags"]
    )
    assert not overlap, f"tags in both tiers: {sorted(overlap)}"


def test_junk_terms_do_not_kill_real_prospect_names(tax):
    """Junk terms are wrapped in \\b(...)\\b so they match whole tokens only.

    funding-sources.md calls this out explicitly: 'press' inside 'compression'
    and 'fund' inside 'fundamental' must NOT drop a real prospect.
    """
    junk = re.compile(r"\b(" + "|".join(tax["junk_terms"]) + r")\b", re.I)
    should_survive = [
        "Compression Dynamics",
        "Fundamental Materials",
        "Airborne Systems",
        "Institutional Battery Co",  # 'institute' must not match 'institutional'
    ]
    for name in should_survive:
        assert not junk.search(name), f"junk filter wrongly drops {name!r}"

    should_drop = [
        "Battery Materials Association",
        "Clean Energy Institute",
        "Acme Ventures",
        "Department of Energy",
    ]
    for name in should_drop:
        assert junk.search(name), f"junk filter should drop {name!r}"


# --- regression guard for the re.escape bug -------------------------------
# The taxonomy _README defines tier entries as REGEX FRAGMENTS: '.' is an
# any-char wildcard. A 2026-08 optimization pass wrapped them in re.escape(),
# which turned '.' into a literal dot and silently demoted whole categories a
# tier (solid-state battery 5 -> 4, grid-scale 4 -> 3). These cases lock the
# documented behaviour so it cannot regress again.
WILDCARD_CASES = [
    ("solid.state batter", "5", "solid state battery developer"),
    ("grid.scale", "4", "grid scale storage integrator"),
    ("long.duration", "4", "long duration energy storage"),
]


@pytest.mark.parametrize("fragment,tier,text", WILDCARD_CASES)
def test_wildcard_fragments_still_match_after_normalization(tax, fragment, tier, text):
    assert fragment in tax["keyword_tiers"][tier], (
        f"{fragment!r} is no longer in tier {tier}; update this test deliberately"
    )
    assert re.compile(fragment, re.I).search(text), (
        f"{fragment!r} must match {text!r} as a regex fragment"
    )
    assert not re.compile(re.escape(fragment), re.I).search(text), (
        f"{fragment!r} escaped would NOT match {text!r} - this is exactly the "
        "regression being guarded against"
    )
