"""
Gaṇa analyzer — groups Laghu-Guru patterns into the 8 traditional Gaṇas.

The 8 Gaṇas (triads of syllables) form the foundation of Sanskrit prosodic
notation. The mnemonic 'yamātārājabhānasalagāḥ' encodes all 8 patterns:

    य (ya)  = LGG    (from ya-mā-tā)
    म (ma)  = GGG    (from mā-tā-rā)
    त (ta)  = GGL    (from tā-rā-ja)
    र (ra)  = GLG    (from rā-ja-bhā)
    ज (ja)  = LGL    (from ja-bhā-na)
    भ (bha) = GLL    (from bhā-na-sa)
    न (na)  = LLL    (from na-sa-la)
    स (sa)  = LLG    (from sa-la-gā)

After grouping into gaṇas of 3, remaining syllables (1 or 2) are noted as:
    ल (la) = L  (single laghu)
    ग (ga) = G  (single guru)
"""

from dataclasses import dataclass, field


# Gaṇa definitions: pattern → (name in Devanagari, name in IAST, name transliterated)
GANA_MAP = {
    "LGG": ("य", "ya", "Ya-gaṇa"),
    "GGG": ("म", "ma", "Ma-gaṇa"),
    "GGL": ("त", "ta", "Ta-gaṇa"),
    "GLG": ("र", "ra", "Ra-gaṇa"),
    "LGL": ("ज", "ja", "Ja-gaṇa"),
    "GLL": ("भ", "bha", "Bha-gaṇa"),
    "LLL": ("न", "na", "Na-gaṇa"),
    "LLG": ("स", "sa", "Sa-gaṇa"),
}

# Single-syllable suffixes
SINGLE_MAP = {
    "L": ("ल", "la", "Laghu"),
    "G": ("ग", "ga", "Guru"),
}


@dataclass
class Gana:
    """Represents a single Gaṇa (triad) or suffix.

    Attributes:
        pattern: The L-G pattern (e.g., 'LGG' or 'L' or 'G').
        name_devanagari: Gaṇa name in Devanagari (e.g., 'य').
        name_iast: Gaṇa name in IAST (e.g., 'ya').
        label: Human-readable label (e.g., 'Ya-gaṇa').
        is_suffix: True if this is a trailing 1-2 syllable suffix, not a full gaṇa.
    """
    pattern: str = ""
    name_devanagari: str = ""
    name_iast: str = ""
    label: str = ""
    is_suffix: bool = False


@dataclass
class GanaResult:
    """Result of Gaṇa analysis for a pāda.

    Attributes:
        ganas: List of Gana objects.
        formula: Gaṇa formula string (e.g., 'ta-ta-ja-ga-ga' for Indravajrā).
        formula_devanagari: Formula in Devanagari (e.g., 'त-त-ज-ग-ग').
        lg_pattern: The original L-G pattern.
    """
    ganas: list = field(default_factory=list)
    formula: str = ""
    formula_devanagari: str = ""
    lg_pattern: str = ""


class GanaAnalyzer:
    """Analyzes L-G patterns and groups them into traditional Gaṇas."""

    def analyze(self, lg_pattern):
        """Analyze an L-G pattern string and decompose into Gaṇas.

        Groups the pattern into triads of 3 syllables, mapping each triad
        to its corresponding Gaṇa. Remaining syllables (1 or 2) are treated
        as suffixes.

        Args:
            lg_pattern: String of 'L' and 'G' characters (e.g., 'GGLGGLGLGG').

        Returns:
            GanaResult with the decomposed Gaṇas and formula.
        """
        if not lg_pattern:
            return GanaResult()

        ganas = []
        i = 0
        n = len(lg_pattern)

        # Group into triads
        while i + 2 < n:
            triad = lg_pattern[i:i + 3]
            if triad in GANA_MAP:
                dev, iast, label = GANA_MAP[triad]
                ganas.append(Gana(
                    pattern=triad,
                    name_devanagari=dev,
                    name_iast=iast,
                    label=label,
                ))
            i += 3

        # Handle remaining 1 or 2 syllables
        remainder = lg_pattern[i:]
        for ch in remainder:
            if ch in SINGLE_MAP:
                dev, iast, label = SINGLE_MAP[ch]
                ganas.append(Gana(
                    pattern=ch,
                    name_devanagari=dev,
                    name_iast=iast,
                    label=label,
                    is_suffix=True,
                ))

        # Build formula strings
        formula_parts = [g.name_iast for g in ganas]
        formula_dev_parts = [g.name_devanagari for g in ganas]

        return GanaResult(
            ganas=ganas,
            formula="-".join(formula_parts),
            formula_devanagari="-".join(formula_dev_parts),
            lg_pattern=lg_pattern,
        )

    def analyze_verse(self, lg_patterns):
        """Analyze L-G patterns for all pādas of a verse.

        Args:
            lg_patterns: List of L-G pattern strings, one per pāda.

        Returns:
            List of GanaResult objects, one per pāda.
        """
        return [self.analyze(pattern) for pattern in lg_patterns]


# Module-level convenience instance
analyzer = GanaAnalyzer()
