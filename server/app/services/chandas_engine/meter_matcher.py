"""
Custom meter matcher — exact and fuzzy pattern matching.

Tier 1: Exact match — O(1) lookup of L-G pattern in the meter database.
Tier 2: Fuzzy match — Levenshtein edit distance (≤ 3 per pāda), returns
        top-3 candidates ranked by similarity.

Note: Tier 3 (LSTM classifier) is implemented in Phase 7, not here.
"""

from dataclasses import dataclass, field
from .meter_db import MeterDatabase, Meter


@dataclass
class MeterMatch:
    """A meter match result.

    Attributes:
        meter: The matched Meter object.
        tier: Which tier identified it (1=exact, 2=fuzzy).
        confidence: Confidence score (0.0 to 1.0).
        edit_distance: Edit distance (0 for exact match).
        matched_pattern: The L-G pattern that was matched against.
    """
    meter: Meter = None
    tier: int = 0
    confidence: float = 0.0
    edit_distance: int = 0
    matched_pattern: str = ""


@dataclass
class MatchResult:
    """Complete result of the meter identification process.

    Attributes:
        matches: List of MeterMatch objects, sorted by confidence.
        best_match: The top match (or None if no match found).
        tier_used: Which tier found the best match (1, 2, or 0 if none).
        input_patterns: The input L-G patterns (one per pāda).
    """
    matches: list = field(default_factory=list)
    best_match: MeterMatch = None
    tier_used: int = 0
    input_patterns: list = field(default_factory=list)


class MeterMatcher:
    """Meter identification engine using exact and fuzzy pattern matching.

    Implements a 2-tier matching system:
        Tier 1: Exact pattern match against 200+ known meters
        Tier 2: Fuzzy match using edit distance with configurable threshold
    """

    def __init__(self, meter_db=None):
        """Initialize the meter matcher.

        Args:
            meter_db: MeterDatabase instance. If None, creates a new one.
        """
        if meter_db is None:
            meter_db = MeterDatabase()
        self.meter_db = meter_db
        self.meter_db.ensure_loaded()

    def identify(self, pada_patterns, full_verse_text=""):
        """Identify the meter from L-G patterns of all pādas.

        Runs Tier 1 (exact) first, then Tier 2 (fuzzy) if no exact match.

        Args:
            pada_patterns: List of L-G pattern strings, one per pāda.
            full_verse_text: Original verse text (for context, not used in matching).

        Returns:
            MatchResult with all matches found.
        """
        if not pada_patterns:
            return MatchResult()

        result = MatchResult(input_patterns=pada_patterns)

        # Tier 1: Exact match
        exact_matches = self._exact_match(pada_patterns)
        if exact_matches:
            result.matches = exact_matches
            result.best_match = exact_matches[0]
            result.tier_used = 1
            return result

        # Tier 2: Fuzzy match
        fuzzy_matches = self._fuzzy_match(pada_patterns)
        if fuzzy_matches:
            result.matches = fuzzy_matches
            result.best_match = fuzzy_matches[0]
            result.tier_used = 2
            return result

        # No match found
        return result

    def _exact_match(self, pada_patterns):
        """Tier 1: Exact pattern match.

        For sama vṛtta: all pādas should match the same pattern.
        For ardhasama: odd and even pādas match separately.
        For Anuṣṭubh: special handling (partial pattern match).

        Args:
            pada_patterns: List of L-G pattern strings.

        Returns:
            List of MeterMatch objects with exact matches.
        """
        matches = []

        # Strategy 1: Try matching each pāda's pattern directly
        for pattern in pada_patterns:
            direct_matches = self.meter_db.get_by_pattern(pattern)
            for meter in direct_matches:
                match = MeterMatch(
                    meter=meter,
                    tier=1,
                    confidence=1.0,
                    edit_distance=0,
                    matched_pattern=pattern,
                )
                if not any(m.meter.id == meter.id for m in matches):
                    matches.append(match)

        # Strategy 2: Check if all pādas have the same pattern (sama vṛtta)
        if len(pada_patterns) >= 2:
            unique_patterns = set(pada_patterns)
            if len(unique_patterns) == 1:
                # All pādas identical — classic sama vṛtta
                pattern = pada_patterns[0]
                for meter in self.meter_db.get_by_pattern(pattern):
                    if meter.category == "sama_vrtta":
                        match = MeterMatch(
                            meter=meter, tier=1, confidence=1.0,
                            edit_distance=0, matched_pattern=pattern,
                        )
                        if not any(m.meter.id == meter.id for m in matches):
                            matches.append(match)

        # Strategy 3: Anuṣṭubh / Śloka detection (special case)
        if len(pada_patterns) >= 2:
            anushtubh_match = self._check_anushtubh(pada_patterns)
            if anushtubh_match:
                if not any(m.meter.id == "anushtubh" for m in matches):
                    matches.append(anushtubh_match)

        return sorted(matches, key=lambda m: m.confidence, reverse=True)

    def _check_anushtubh(self, pada_patterns):
        """Special check for Anuṣṭubh/Śloka meter.

        Anuṣṭubh rules:
        - Each pāda has 8 syllables
        - 5th is always Laghu (L), 6th is always Guru (G)
        - 7th is Laghu (L) in even pādas (2nd, 4th)
        - 7th is Guru (G) in odd pādas (1st, 3rd)
        - 8th is Guru (G) by convention
        - So positions 5-8 (indices 4-7) must be:
          - Even pādas: LGLG
          - Odd pādas: LGGG

        Returns:
            MeterMatch if the verse matches Anuṣṭubh, else None.
        """
        # Check syllable count: all pādas should have 8 syllables
        if not all(len(p) == 8 for p in pada_patterns):
            return None

        # Check even pādas (indices 1, 3): last 4 should be LGLG
        even_ok = True
        for i in [1, 3]:
            if i < len(pada_patterns):
                pada = pada_patterns[i]
                if len(pada) >= 8:
                    if pada[4:8] != "LGLG":
                        even_ok = False

        if even_ok:
            meter = self.meter_db.get_by_id("anushtubh")
            if meter:
                return MeterMatch(
                    meter=meter,
                    tier=1,
                    confidence=0.95,
                    edit_distance=0,
                    matched_pattern="Anuṣṭubh (8-syllable, even pāda: xxxxLGLG)",
                )

        return None

    def _fuzzy_match(self, pada_patterns, max_distance=3, top_k=3):
        """Tier 2: Fuzzy pattern match using Levenshtein distance.

        Compares the input pattern against all known meters and returns
        the top-k closest matches within the distance threshold.

        Args:
            pada_patterns: List of L-G pattern strings.
            max_distance: Maximum allowed edit distance per pāda.
            top_k: Number of top matches to return.

        Returns:
            List of MeterMatch objects sorted by confidence.
        """
        candidates = []

        # Get all meters with the same syllable count
        for pattern in pada_patterns:
            syllable_count = len(pattern)
            potential_meters = self.meter_db.get_by_syllable_count(syllable_count)

            for meter in potential_meters:
                # Skip meters already processed
                if any(c.meter.id == meter.id for c in candidates):
                    continue

                # Calculate edit distance
                if meter.pattern:
                    dist = self._levenshtein_distance(pattern, meter.pattern)
                    if dist <= max_distance:
                        confidence = 1.0 - (dist / max(len(pattern), len(meter.pattern)))
                        candidates.append(MeterMatch(
                            meter=meter,
                            tier=2,
                            confidence=confidence,
                            edit_distance=dist,
                            matched_pattern=meter.pattern,
                        ))

        # Also check all patterns in the database (not just same syllable count)
        all_patterns = self.meter_db.get_all_patterns()
        for db_pattern, meter_ids in all_patterns.items():
            for pattern in pada_patterns:
                if abs(len(pattern) - len(db_pattern)) <= max_distance:
                    dist = self._levenshtein_distance(pattern, db_pattern)
                    if dist <= max_distance:
                        for meter_id in meter_ids:
                            if any(c.meter.id == meter_id for c in candidates):
                                continue
                            meter = self.meter_db.get_by_id(meter_id)
                            if meter:
                                confidence = 1.0 - (dist / max(len(pattern), len(db_pattern)))
                                candidates.append(MeterMatch(
                                    meter=meter,
                                    tier=2,
                                    confidence=confidence,
                                    edit_distance=dist,
                                    matched_pattern=db_pattern,
                                ))

        # Sort by confidence (descending) and return top-k
        candidates.sort(key=lambda m: m.confidence, reverse=True)

        # Deduplicate by meter ID
        seen = set()
        unique = []
        for c in candidates:
            if c.meter.id not in seen:
                seen.add(c.meter.id)
                unique.append(c)

        return unique[:top_k]

    @staticmethod
    def _levenshtein_distance(s1, s2):
        """Calculate the Levenshtein edit distance between two strings.

        Args:
            s1: First string.
            s2: Second string.

        Returns:
            Integer edit distance.
        """
        if len(s1) < len(s2):
            return MeterMatcher._levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        prev_row = list(range(len(s2) + 1))

        for i, c1 in enumerate(s1):
            curr_row = [i + 1]
            for j, c2 in enumerate(s2):
                # Cost is 0 if characters match, 1 otherwise
                insertions = prev_row[j + 1] + 1
                deletions = curr_row[j] + 1
                substitutions = prev_row[j] + (0 if c1 == c2 else 1)
                curr_row.append(min(insertions, deletions, substitutions))
            prev_row = curr_row

        return prev_row[-1]
