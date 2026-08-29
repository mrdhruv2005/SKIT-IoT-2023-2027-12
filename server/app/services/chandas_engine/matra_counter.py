"""
Mātrā (mora) counter for Jāti meters.

In Jāti meters (like Āryā, Gīti), the identification is based on the total
moraic weight (mātrā count) per pāda, rather than a fixed syllable pattern.

Rules:
    - Laghu (L) = 1 mātrā
    - Guru (G) = 2 mātrā

This module counts the total mātrā per pāda and per verse, which is used
by the meter matcher to identify Jāti meters.
"""

from dataclasses import dataclass, field


@dataclass
class MatraResult:
    """Mātrā count result for a single pāda.

    Attributes:
        lg_pattern: The L-G pattern string.
        matra_count: Total mātrā count.
        matra_per_syllable: List of mātrā values for each syllable.
    """
    lg_pattern: str = ""
    matra_count: int = 0
    matra_per_syllable: list = field(default_factory=list)


class MatraCounter:
    """Counts mātrā (morae) for Sanskrit syllable patterns."""

    # Mātrā values
    LAGHU_MATRA = 1
    GURU_MATRA = 2

    def count_pada(self, lg_pattern):
        """Count total mātrā for a single pāda.

        Args:
            lg_pattern: L-G pattern string (e.g., 'LGGLGGL').

        Returns:
            MatraResult with the total count and per-syllable values.
        """
        if not lg_pattern:
            return MatraResult()

        per_syllable = []
        total = 0

        for ch in lg_pattern:
            if ch == "G":
                per_syllable.append(self.GURU_MATRA)
                total += self.GURU_MATRA
            elif ch == "L":
                per_syllable.append(self.LAGHU_MATRA)
                total += self.LAGHU_MATRA

        return MatraResult(
            lg_pattern=lg_pattern,
            matra_count=total,
            matra_per_syllable=per_syllable,
        )

    def count_verse(self, lg_patterns):
        """Count mātrā for all pādas of a verse.

        Args:
            lg_patterns: List of L-G pattern strings, one per pāda.

        Returns:
            List of MatraResult objects, one per pāda.
        """
        return [self.count_pada(p) for p in lg_patterns]

    def total_verse_matra(self, lg_patterns):
        """Get total mātrā count for the entire verse.

        Args:
            lg_patterns: List of L-G pattern strings.

        Returns:
            Total mātrā count across all pādas.
        """
        return sum(r.matra_count for r in self.count_verse(lg_patterns))


# Module-level convenience instance
counter = MatraCounter()
