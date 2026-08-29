"""Tests for the MeterMatcher module."""

import pytest
from app.services.chandas_engine import MeterMatcher, MeterDatabase


@pytest.fixture
def matcher():
    db = MeterDatabase()
    db.load()
    return MeterMatcher(db)


def test_exact_match_sama_vrtta(matcher):
    # Indravajra: GGLGGLGLGG
    padas = ["GGLGGLGLGG"] * 4
    result = matcher.identify(padas)
    
    assert result.tier_used == 1
    assert result.best_match is not None
    assert result.best_match.meter.id == "indravajra"


def test_anushtubh_match(matcher):
    # Anushtubh even padas end in LGLG
    # Odd padas end in LGGG
    padas = [
        "GGGGLGGG",  # odd: 5-L, 6-G, 7-G, 8-G -> wait, GGGGLGGG means 5 is G!
                     # BG 1.1 pada 1 is: dharma(GG)-ksetre(GG)-kuru(LL)-ksetre(GG) -> GGGGLGGG.
                     # 5th is L, 6th is G, 7th is G, 8th is G.
                     # wait, GGGGLGGG -> 1=G, 2=G, 3=G, 4=G, 5=L, 6=G, 7=G, 8=G. Yes!
        "LLGGLGLG",  # even: 5-L, 6-G, 7-L, 8-G
        "GLGGLGGG",  # odd: 5-L, 6-G, 7-G, 8-G
        "LLGLLGLG",  # even: 5-L, 6-G, 7-L, 8-G
    ]
    result = matcher.identify(padas)
    
    assert result.tier_used == 1
    assert result.best_match is not None
    assert result.best_match.meter.id == "anushtubh"


def test_fuzzy_match(matcher):
    # Indravajra with 1 error: GGLGGLGLGL (last is L instead of G)
    padas = ["GGLGGLGLGL"] * 4
    result = matcher.identify(padas)
    
    assert result.tier_used == 2
    assert result.best_match is not None
    assert result.best_match.meter.id == "indravajra"
    assert result.best_match.edit_distance == 1


def test_no_match(matcher):
    # 30 syllables (no meter has this length so it won't fuzzy match within edit distance 3)
    padas = ["LLLLL" * 6] * 4
    result = matcher.identify(padas)
    
    assert result.tier_used == 0
    assert result.best_match is None
