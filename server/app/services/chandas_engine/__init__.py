"""
Chandas engine package — custom-built meter identification engine.

Exposes the main engine classes for clean imports:
    from app.services.chandas_engine import SyllableParser, LaghuGuruClassifier, ...
"""

from .syllable_parser import SyllableParser, Syllable, ParseResult
from .laghu_guru import LaghuGuruClassifier, ClassifiedSyllable, LGResult, LAGHU, GURU
from .gana_analyzer import GanaAnalyzer, Gana, GanaResult
from .matra_counter import MatraCounter, MatraResult
from .meter_db import MeterDatabase, Meter
from .meter_matcher import MeterMatcher, MeterMatch, MatchResult

__all__ = [
    # Core classes
    "SyllableParser",
    "LaghuGuruClassifier",
    "GanaAnalyzer",
    "MatraCounter",
    "MeterDatabase",
    "MeterMatcher",
    # Data classes
    "Syllable",
    "ParseResult",
    "ClassifiedSyllable",
    "LGResult",
    "Gana",
    "GanaResult",
    "MatraResult",
    "Meter",
    "MeterMatch",
    "MatchResult",
    # Constants
    "LAGHU",
    "GURU",
]
