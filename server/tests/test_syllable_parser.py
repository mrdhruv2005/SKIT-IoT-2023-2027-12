"""Tests for the SyllableParser module."""

import pytest
from app.services.chandas_engine import SyllableParser


@pytest.fixture
def parser():
    return SyllableParser()


def test_empty_string(parser):
    result = parser.parse("")
    assert result.total_syllables == 0
    assert len(result.padas) == 0


def test_simple_word(parser):
    # राम (rāma) -> रा - म
    result = parser.parse("राम")
    assert result.total_syllables == 2
    syllables = result.syllables_by_pada[0]
    assert syllables[0].text == "रा"
    assert syllables[0].is_long_vowel is True
    assert syllables[1].text == "म"
    assert syllables[1].is_long_vowel is False


def test_halant(parser):
    # वाक् (vāk) -> वाक् (1 syllable)
    result = parser.parse("वाक्")
    assert result.total_syllables == 1
    syl = result.syllables_by_pada[0][0]
    assert syl.text == "वाक्"


def test_conjunct_consonants(parser):
    # धर्म (dharma) -> ध - र्म
    result = parser.parse("धर्म")
    assert result.total_syllables == 2
    syllables = result.syllables_by_pada[0]
    assert syllables[0].text == "ध"
    assert syllables[1].text == "र्म"
    
    # Check conjunct marking
    assert syllables[0].consonant_cluster_follows is True
    assert syllables[1].consonant_cluster_follows is False


def test_anusvara(parser):
    # हंस (haṃsa) -> हं - स
    result = parser.parse("हंस")
    assert result.total_syllables == 2
    syllables = result.syllables_by_pada[0]
    assert syllables[0].text == "हं"
    assert syllables[0].has_anusvara is True
    assert syllables[1].text == "स"


def test_visarga(parser):
    # रामः (rāmaḥ) -> रा - मः
    result = parser.parse("रामः")
    assert result.total_syllables == 2
    syllables = result.syllables_by_pada[0]
    assert syllables[1].text == "मः"
    assert syllables[1].has_visarga is True


def test_independent_vowels(parser):
    # इह (iha) -> इ - ह
    result = parser.parse("इह")
    assert result.total_syllables == 2
    syllables = result.syllables_by_pada[0]
    assert syllables[0].text == "इ"
    assert syllables[0].is_long_vowel is False


def test_avagraha(parser):
    # सोऽहम् (so'ham) -> सो - ऽ - हम्
    result = parser.parse("सोऽहम्")
    assert result.total_syllables == 3
    syllables = result.syllables_by_pada[0]
    assert syllables[0].text == "सो"
    assert syllables[1].text == "ऽ"
    assert syllables[2].text == "हम्"


def test_danda_splitting(parser):
    # रामः। कृष्णः॥ -> 2 padas
    result = parser.parse("रामः। कृष्णः॥")
    assert len(result.padas) == 2
    assert result.padas[0] == "रामः"
    assert result.padas[1] == "कृष्णः"


def test_anushtubh_auto_splitting(parser):
    # 16 syllables without danda should auto-split into 8 + 8
    # dharma-kṣetre kuru-kṣetre samavetā yuyutsavaḥ (16 syllables)
    text = "धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः"
    result = parser.parse(text)
    assert len(result.padas) == 2
    assert len(result.syllables_by_pada[0]) == 8
    assert len(result.syllables_by_pada[1]) == 8
    assert result.padas[0] == "धर्मक्षेत्रेकुरुक्षेत्रे"
    assert result.padas[1] == "समवेतायुयुत्सवः"
