"""Tests for the JE Seq. 1 editorial linter.

The linter gates outbound cold-email copy, so a false PASS ships a rule
violation to a prospect and a false FAIL erodes trust in the tool until it
gets ignored. Both directions are tested.
"""

import importlib.util
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".claude/skills/je-outreach-seq1/scripts/lint_draft.py"


def _load():
    spec = importlib.util.spec_from_file_location("lint_draft", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lint = _load()


def body_results(text, tight=False):
    rep = lint.Report()
    lint.check_body(text, rep, tight)
    return {name: ok for ok, name, _ in rep.rows}


def subject_results(text):
    rep = lint.Report()
    lint.check_subject(text, rep)
    return {name: ok for ok, name, _ in rep.rows}


GOOD_BODY = (
    "Congratulations on the Activate fellowship. Renesin was one of the eight "
    "founders named at Activate Houston in the 2026 cohort.\n\n"
    "I am Riley Jackson at Johnston Engineering (JE), a 23-person mechanical "
    "engineering firm in Spokane.\n\n"
    "Where is Renesin actually stuck right now, the material or the proof?"
)


def test_script_exists():
    assert SCRIPT.is_file(), f"linter missing at {SCRIPT}"


def test_clean_body_passes_every_check():
    assert all(body_results(GOOD_BODY).values())


def test_clean_subject_passes_every_check():
    subject = "Custom Automation and Test Hardware for the Tucson Cell Line"
    assert all(subject_results(subject).values())


# --- body checks -----------------------------------------------------------

@pytest.mark.parametrize("dash", ["—", "–", "―"])
def test_dashes_are_caught(dash):
    text = GOOD_BODY.replace("Spokane.", "Spokane %s a good city." % dash)
    assert body_results(text)["body/no-em-dash"] is False


@pytest.mark.parametrize(
    "opener",
    ["Hi Steve,", "Hello there,", "Hey Chao,", "Dear Dr. Hui,",
     "Good morning,", "Greetings,"],
)
def test_greeting_lines_are_caught(opener):
    assert body_results(opener + "\n\n" + GOOD_BODY)["body/no-greeting"] is False


def test_banned_phrase_is_caught_case_insensitively():
    text = (
        "We are Interested In Learning More About Your Development Priorities."
        "\n\nSecond paragraph."
    )
    assert body_results(text)["body/banned-phrase"] is False


def test_length_limit_and_tight_variant():
    body = "word. " * 400          # 2400 chars, over both limits
    assert body_results(body)["body/length"] is False
    ok = "x" * 1960 + "\n\nsecond"  # under 2000, over the tight 1950
    assert body_results(ok)["body/length"] is True
    assert body_results(ok, tight=True)["body/length"] is False


def test_missing_paragraph_breaks_caught():
    single = "One paragraph with no blank line separation at all."
    assert body_results(single)["body/paragraph-breaks"] is False


@pytest.mark.parametrize("bullet", ["- thermal FEA", "* thermal FEA",
                                    "1. thermal FEA", "2) thermal FEA"])
def test_bullets_are_caught(bullet):
    text = "Intro paragraph.\n\n" + bullet + "\n\nClosing question?"
    assert body_results(text)["body/no-bullets"] is False


# --- signature: the regression that a tail-only check missed ---------------

def test_signature_at_end_is_caught():
    text = GOOD_BODY + "\n\nBest,\nRiley Jackson\nJohnston Engineering"
    assert body_results(text)["body/no-signature"] is False


def test_signature_is_caught_even_when_text_follows_it():
    """Regression: the original implementation only inspected the last three
    non-empty lines, so any sign-off with more than three lines after it went
    undetected. Keep enough trailing lines here to push the sign-off out of
    that window, otherwise this test passes against the bug it guards."""
    trailing = "\n\n".join(
        "Trailing paragraph number %d that follows the signature." % i
        for i in range(1, 6)
    )
    text = GOOD_BODY + "\n\nBest,\nRiley Jackson\n\n" + trailing
    assert body_results(text)["body/no-signature"] is False


@pytest.mark.parametrize(
    "phrase",
    [
        "The best path is thermal FEA first.",
        "Thanks for reading this far.",
        "Regards vary between reviewers on this point.",
        "We sincerely think the joint is the constraint.",
    ],
)
def test_signoff_words_mid_sentence_do_not_false_positive(phrase):
    text = phrase + "\n\nDoes that track?"
    assert body_results(text)["body/no-signature"] is True


# --- subject checks --------------------------------------------------------

def test_retired_subject_format_is_caught():
    subject = "Johnston Engineering - Mechanical Engineering Support for Acme"
    assert subject_results(subject)["subject/retired-format"] is False


def test_lowercase_principal_words_caught():
    assert subject_results("custom hardware for acme")[
        "subject/title-case"] is False


def test_small_words_may_stay_lowercase_mid_title():
    subject = "From a Single Cell to a Full Stack at Nexceris"
    assert subject_results(subject)["subject/title-case"] is True


@pytest.mark.parametrize(
    "subject",
    [
        "The MILAbot Joint and the Pour It Has to Survive",
        "From a Single Cell to a 5.5 GWh Line at ABF",
        "ANSYS CFD Capacity for the SOEC Stack Line",
    ],
)
def test_acronyms_and_internal_caps_are_not_case_errors(subject):
    assert subject_results(subject)["subject/title-case"] is True


def test_em_dash_in_subject_is_caught():
    assert subject_results("Thermal Capacity — for Acme")[
        "subject/no-em-dash"] is False


# --- CLI contract ----------------------------------------------------------

def _run(args, stdin=None):
    return subprocess.run(
        [sys.executable, str(SCRIPT)] + args,
        input=stdin, capture_output=True, text=True,
    )


def test_cli_exits_zero_on_clean_draft(tmp_path):
    path = tmp_path / "draft.txt"
    path.write_text(GOOD_BODY, encoding="utf-8")
    res = _run(["--subject", "A Clean Tailored Subject Line",
                "--body-file", str(path)])
    assert res.returncode == 0, res.stdout


def test_cli_exits_nonzero_on_violation(tmp_path):
    path = tmp_path / "draft.txt"
    path.write_text("Hi Steve,\n\n" + GOOD_BODY, encoding="utf-8")
    res = _run(["--body-file", str(path)])
    assert res.returncode == 1
    assert "body/no-greeting" in res.stdout


def test_cli_reads_stdin():
    res = _run(["--body-file", "-"], stdin=GOOD_BODY)
    assert res.returncode == 0, res.stdout


def test_cli_requires_an_argument():
    assert _run([]).returncode == 2


def test_cli_reports_missing_file(tmp_path):
    res = _run(["--body-file", str(tmp_path / "nope.txt")])
    assert res.returncode == 2
    assert "cannot read body file" in res.stderr
