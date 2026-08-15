"""Tests for the LaghuGuruClassifier module."""

import pytest
from app.services.chandas_engine import LaghuGuruClassifier, SyllableParser, LAGHU, GURU


@pytest.fixture
def parser():
    return SyllableParser()


@pytest.fixture
def classifier():
    return LaghuGuruClassifier()


def get_pattern(text, parser, classifier):
    result = parser.parse(text)
    lg_results = classifier.classify_verse(result.syllables_by_pada)
    return lg_results[0].pattern if lg_results else ""


def test_short_vowel(parser, classifier):
    # क (ka) -> L (but since it is the only syllable, it is pada-final -> G)
    assert get_pattern("क", parser, classifier) == GURU


def test_long_vowel(parser, classifier):
    # का (kā) -> G
    assert get_pattern("का", parser, classifier) == GURU
    # के (ke) -> G
    assert get_pattern("के", parser, classifier) == GURU


def test_anusvara(parser, classifier):
    # कं (kaṃ) -> G
    assert get_pattern("कं", parser, classifier) == GURU


def test_visarga(parser, classifier):
    # कः (kaḥ) -> G
    assert get_pattern("कः", parser, classifier) == GURU


def test_samyoga(parser, classifier):
    # अ (a) is short, but followed by त्त (tta) which is a conjunct -> G
    # त्त (tta) is pada-final -> G
    assert get_pattern("अत्त", parser, classifier) == GURU + GURU


def test_pada_final(parser, classifier):
    # इ (i) is short. In "इ", it's pada-final, so it becomes Guru.
    assert get_pattern("इ", parser, classifier) == GURU
    
    # "इति" -> i is L, ti is pada-final so it becomes G.
    assert get_pattern("इति", parser, classifier) == LAGHU + GURU


def test_bg_1_1(parser, classifier):
    # धर्मक्षेत्रे (dharma-kṣetre) 
    # ध(G due to rma) र्म(G due to kṣe) क्षे(G due to tre) त्रे(G)
    p1 = get_pattern("धर्मक्षेत्रे", parser, classifier)
    assert p1 == "GGGG"
