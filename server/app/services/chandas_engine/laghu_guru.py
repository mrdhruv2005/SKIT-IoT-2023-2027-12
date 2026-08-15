"""
Custom Laghu-Guru (Light-Heavy) syllable classifier — built from scratch.

Implements phonological rules from Piṅgala's Chandaḥśāstra for classifying
each syllable as Laghu (light/short, L) or Guru (heavy/long, G).

Rules:
    Guru (G) — a syllable is heavy if:
        1. It contains a long vowel (ā, ī, ū, ṝ, ḹ, e, ai, o, au)
        2. It contains a short vowel followed by a consonant cluster (saṃyoga)
        3. It ends with visarga (ः)
        4. It ends with anusvāra (ं)
        5. It is the final syllable of a pāda (by convention, marked as G)

    Laghu (L) — everything else:
        A syllable with a short vowel (a, i, u, ṛ, ḷ) and no following
        consonant cluster, no visarga, no anusvāra.
"""

from dataclasses import dataclass, field
from .syllable_parser import Syllable


# Classification symbols
LAGHU = "L"  # Light/short syllable (लघु)
GURU = "G"   # Heavy/long syllable (गुरु)


@dataclass
class ClassifiedSyllable:
    """A syllable with its Laghu-Guru classification.

    Attributes:
        syllable: The original Syllable object.
        classification: 'L' (Laghu) or 'G' (Guru).
        reason: Human-readable reason for the classification.
    """
    syllable: Syllable
    classification: str = ""
    reason: str = ""


@dataclass
class LGResult:
    """Result of Laghu-Guru classification for a pāda.

    Attributes:
        classified_syllables: List of ClassifiedSyllable objects.
        pattern: The L-G pattern string (e.g., 'GLGGLLGL').
        syllable_count: Number of syllables in this pāda.
    """
    classified_syllables: list = field(default_factory=list)
    pattern: str = ""
    syllable_count: int = 0


class LaghuGuruClassifier:
    """Classifies Sanskrit syllables as Laghu (L) or Guru (G).

    Uses the standard prosodic rules from Piṅgala's Chandaḥśāstra.
    """

    def classify_pada(self, syllables):
        """Classify all syllables in a single pāda.

        Args:
            syllables: List of Syllable objects from the SyllableParser.

        Returns:
            LGResult with classified syllables and the L-G pattern string.
        """
        if not syllables:
            return LGResult()

        classified = []
        for i, syl in enumerate(syllables):
            cls, reason = self._classify_one(syl)
            classified.append(ClassifiedSyllable(
                syllable=syl,
                classification=cls,
                reason=reason,
            ))

        pattern = "".join(cs.classification for cs in classified)

        return LGResult(
            classified_syllables=classified,
            pattern=pattern,
            syllable_count=len(classified),
        )

    def classify_verse(self, syllables_by_pada):
        """Classify all syllables across all pādas of a verse.

        Args:
            syllables_by_pada: List of lists of Syllable objects (one list per pāda).

        Returns:
            List of LGResult objects, one per pāda.
        """
        return [self.classify_pada(pada) for pada in syllables_by_pada]

    def get_verse_pattern(self, syllables_by_pada):
        """Get the combined L-G pattern for the entire verse.

        Args:
            syllables_by_pada: List of lists of Syllable objects.

        Returns:
            List of pattern strings, one per pāda.
        """
        results = self.classify_verse(syllables_by_pada)
        return [r.pattern for r in results]

    def _classify_one(self, syllable):
        """Classify a single syllable.

        Args:
            syllable: A Syllable object.

        Returns:
            Tuple of (classification, reason).
        """
        # Rule 1: Long vowel → Guru
        if syllable.is_long_vowel:
            return GURU, "Long vowel (dīrgha svara)"

        # Rule 2: Visarga → Guru
        if syllable.has_visarga:
            return GURU, "Visarga (ः) present"

        # Rule 3: Anusvāra → Guru
        if syllable.has_anusvara:
            return GURU, "Anusvāra (ं) present"

        # Rule 4: Chandrabindu → Guru (nasalization makes heavy)
        if syllable.has_chandrabindu:
            return GURU, "Chandrabindu (ँ) present"

        # Rule 5: Consonant cluster follows (saṃyoga) → Guru
        if syllable.consonant_cluster_follows:
            return GURU, "Saṃyoga (consonant cluster follows)"

        # Rule 6: Pāda-final syllable → Guru by convention
        if syllable.is_pada_final:
            return GURU, "Pāda-final syllable (guru by convention)"

        # Default: Short vowel, no special conditions → Laghu
        return LAGHU, "Short vowel (hrasva svara), no saṃyoga"


# Module-level convenience instance
classifier = LaghuGuruClassifier()
