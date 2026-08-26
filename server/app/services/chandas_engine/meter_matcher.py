"""
Custom meter matcher — exact and fuzzy pattern matching.

Tier 1: Exact match — O(1) lookup of L-G pattern in the meter database.
Tier 2: Fuzzy match — Levenshtein edit distance (≤ 3 per pāda), returns
        top-3 candidates ranked by similarity.

Note: Tier 3 (LSTM classifier) is implemented in Phase 7, not here.
"""

from dataclasses import dataclass, field
from .meter_db import MeterDatabase, Meter
from app.services.cache_service import cache


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
            
        # Create a cache key from the patterns
        pattern_key = "|".join(pada_patterns)
        
        # Check cache first
        cached_result = cache.get_meter_pattern(pattern_key)
        if cached_result:
            # Reconstruct the MatchResult from the cached dict
            result = MatchResult(input_patterns=pada_patterns)
            result.tier_used = cached_result.get("tier_used", 0)
            
            # Reconstruct matches
            for m_dict in cached_result.get("matches", []):
                # We need to recreate the Meter object from its dict representation
                meter_dict = m_dict.get("meter", {})
                meter = Meter(
                    id=meter_dict.get("id", ""),
                    name_iast=meter_dict.get("name_iast", ""),
                    name_devanagari=meter_dict.get("name_devanagari", ""),
                    name_english=meter_dict.get("name_english", ""),
                    category=meter_dict.get("category", ""),
                    syllables_per_pada=meter_dict.get("syllables_per_pada", 0),
                    pattern=meter_dict.get("pattern", ""),
                    gana_formula=meter_dict.get("gana_formula", ""),
                    description=meter_dict.get("description", ""),
                    example_verse=meter_dict.get("example_verse", ""),
                    example_source=meter_dict.get("example_source", "")
                )
                
                match = MeterMatch(
                    meter=meter,
                    tier=m_dict.get("tier", 0),
                    confidence=m_dict.get("confidence", 0.0),
                    edit_distance=m_dict.get("edit_distance", 0),
                    matched_pattern=m_dict.get("matched_pattern", "")
                )
                result.matches.append(match)
                
            if result.matches:
                result.best_match = result.matches[0]
                
            return result

        result = MatchResult(input_patterns=pada_patterns)

        # Tier 1: Exact match
        exact_matches = self._exact_match(pada_patterns)
        if exact_matches:
            result.matches = exact_matches
            result.best_match = exact_matches[0]
            result.tier_used = 1
            self._cache_result(pattern_key, result)
            return result

        # Tier 2: Fuzzy match
        fuzzy_matches = self._fuzzy_match(pada_patterns)
        if fuzzy_matches:
            result.matches = fuzzy_matches
            result.best_match = fuzzy_matches[0]
            result.tier_used = 2
            self._cache_result(pattern_key, result)
            return result

        # No match found
        self._cache_result(pattern_key, result)
        return result

    def _cache_result(self, pattern_key, result):
        """Helper to serialize and cache a MatchResult."""
        try:
            cached_data = {
                "tier_used": result.tier_used,
                "matches": []
            }
            for match in result.matches:
                cached_data["matches"].append({
                    "meter": match.meter.to_dict() if hasattr(match.meter, "to_dict") else match.meter.__dict__,
                    "tier": match.tier,
                    "confidence": match.confidence,
                    "edit_distance": match.edit_distance,
                    "matched_pattern": match.matched_pattern
                })
            cache.cache_meter_pattern(pattern_key, cached_data)
        except Exception:
            pass # Ignore caching errors to not break the flow

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
